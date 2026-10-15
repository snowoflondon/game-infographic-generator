"""Deterministic, contrast-checked presentation colors from local artwork."""

from collections import Counter
from colorsys import rgb_to_hls
from io import BytesIO

from PIL import Image, ImageOps

BACKGROUND = '#f5f3ee'
PRIMARY = '#252b2c'
SECONDARY = '#5d6866'
PANEL = '#eeece6'
DIVIDER = '#d4d8d1'
FALLBACK_ACCENT = '#375b68'


def contrast(first: str, second: str) -> float:
    """Return the WCAG relative-luminance contrast ratio for two hex colors."""
    def luminance(color: str) -> float:
        values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values]
        return sum(v * weight for v, weight in zip(linear, (0.2126, 0.7152, 0.0722)))
    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def extract_theme(artwork: bytes | None) -> dict[str, str]:
    """Decode a copy, sample a restrained palette, and select accessible accents.

    Invalid artwork raises an image error; fallback is only for valid images
    without suitable colors. Original bytes are never altered.
    """
    if artwork is None:
        return dict(background=BACKGROUND, primary=PRIMARY, secondary=SECONDARY,
                    panel=PANEL, divider=DIVIDER, accent=FALLBACK_ACCENT, on_accent='#ffffff')
    with Image.open(BytesIO(artwork)) as image:
        image.load()
        sample = ImageOps.exif_transpose(image).convert('RGBA')
        # Nearest sampling avoids manufacturing colors at transparent boundaries.
        sample.thumbnail((128, 128), Image.Resampling.NEAREST)
        pixels = sample.load()
        counts = Counter(
            tuple((channel // 16) * 16 + 8 for channel in pixel[:3])
            for y in range(sample.height) for x in range(sample.width)
            for pixel in [pixels[x, y]] if pixel[3] >= 240
        )
    candidates = []
    for rgb, count in counts.items():
        _, lightness, saturation = rgb_to_hls(*(v / 255 for v in rgb))
        color = '#{:02x}{:02x}{:02x}'.format(*rgb)
        if 0.18 <= saturation <= 0.8 and 0.12 <= lightness <= 0.75 and contrast(color, BACKGROUND) >= 4.5:
            candidates.append((count * (0.5 + saturation), color))
    # Color string breaks equal-ranking ties reproducibly.
    accent = sorted(candidates, key=lambda item: (-item[0], item[1]))[0][1] if candidates else FALLBACK_ACCENT
    on_accent = max((PRIMARY, '#ffffff'), key=lambda color: contrast(color, accent))
    return dict(background=BACKGROUND, primary=PRIMARY, secondary=SECONDARY,
                panel=PANEL, divider=DIVIDER, accent=accent, on_accent=on_accent)
