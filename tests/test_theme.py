"""Color selection without generating infographic images."""
from io import BytesIO

import pytest
from PIL import Image

from game_infographic_generator.rendering.theme import (
    BACKGROUND, PRIMARY, SECONDARY, PANEL, FALLBACK_ACCENT, contrast, extract_theme,
)


def image_bytes(color):
    buffer = BytesIO()
    Image.new('RGBA', (32, 32), color).save(buffer, format='PNG')
    return buffer.getvalue()


def test_color_selection_and_contrast():
    artwork = image_bytes((45, 90, 120, 255))
    theme = extract_theme(artwork)
    assert theme['accent'] != FALLBACK_ACCENT
    assert contrast(theme['accent'], BACKGROUND) >= 4.5
    assert contrast(theme['on_accent'], theme['accent']) >= 4.5
    assert extract_theme(artwork) == theme
    assert theme['background'] == BACKGROUND
    assert theme['primary'] == PRIMARY
    assert theme['secondary'] == SECONDARY
    assert theme['panel'] == PANEL


@pytest.mark.parametrize('color', [(128, 128, 128, 255), (255, 255, 255, 255), (45, 90, 120, 0), (255, 0, 0, 255)])
def test_unsuitable_palette_fallback(color):
    theme = extract_theme(image_bytes(color))
    assert theme['accent'] == FALLBACK_ACCENT
    assert contrast(theme['accent'], BACKGROUND) >= 4.5
    assert contrast(theme['on_accent'], theme['accent']) >= 4.5


def test_known_contrast():
    assert contrast('#000000', '#ffffff') == pytest.approx(21)
    assert contrast('#375b68', '#375b68') == pytest.approx(1)


def test_invalid_image_is_not_fallback():
    with pytest.raises(OSError):
        extract_theme(b'not an image')


def test_palette_tie_is_deterministic():
    image = Image.new('RGB', (32, 32), (45, 90, 120))
    image.paste((120, 65, 90), (16, 0, 32, 32))
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    assert extract_theme(buffer.getvalue()) == extract_theme(buffer.getvalue())
