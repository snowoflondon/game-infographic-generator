"""Generate editorial HTML and capture it with Chromium."""

import base64
import struct
import os
import tempfile
import logging
from importlib.resources import files
from pathlib import Path

from jinja2 import Environment, StrictUndefined
from playwright.sync_api import Error as PlaywrightError, sync_playwright

from ..models import GameMetadata
from .theme import extract_theme
from .platforms import format_platforms
from .presentation import ArtworkPresentation


class RenderingError(RuntimeError):
    """An infographic could not be rendered."""


def build_html(metadata: GameMetadata, artwork: Path | None = None,
               presentation: ArtworkPresentation | None = None) -> str:
    """Build escaped, self-contained HTML from validated metadata."""
    if artwork is None and presentation is not None:
        raise RenderingError('Presentation copy is only supported with --artwork')
    if artwork is not None:
        if presentation is None:
            raise RenderingError('Artwork mode requires condensed copy via --presentation')
        if bool(metadata.description) != bool(presentation.overview):
            raise RenderingError('Supply an overview exactly when the source description is available')
        sentiment = metadata.player_sentiment
        if bool(sentiment and sentiment.positives) != bool(presentation.highlights):
            raise RenderingError('Supply highlights exactly when source positives are available')
        if bool(sentiment and sentiment.negatives) != bool(presentation.criticisms):
            raise RenderingError('Supply criticisms exactly when source negatives are available')
    image = None
    theme = extract_theme(None)
    if artwork is not None:
        artwork = Path(artwork)
        mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".webp": "image/webp"}.get(artwork.suffix.lower())
        if mime is None:
            raise RenderingError("Artwork must be a local PNG, JPEG, or WebP image")
        try:
            data = artwork.read_bytes()
        except OSError as exc:
            raise RenderingError(f"Cannot read artwork '{artwork}': {exc}") from exc
        valid_header = (
            mime == "image/png" and data.startswith(b"\x89PNG\r\n\x1a\n") or
            mime == "image/jpeg" and data.startswith(b"\xff\xd8\xff") or
            mime == "image/webp" and data.startswith(b"RIFF") and data[8:12] == b"WEBP"
        )
        if not valid_header:
            raise RenderingError(f"Artwork '{artwork}' has an invalid or corrupt image header; cannot be decoded")
        try:
            theme = extract_theme(data)
        except (OSError, ValueError) as exc:
            raise RenderingError(f"Artwork '{artwork}' cannot be decoded: {exc}") from exc
        image = f"data:{mime};base64," + base64.b64encode(data).decode("ascii")
    resources = files(__package__).joinpath("templates")
    env = Environment(autoescape=True, undefined=StrictUndefined)
    template = env.from_string(resources.joinpath("single_game.html.j2").read_text(encoding="utf-8"))
    return template.render(game=metadata, platforms_display=format_platforms(metadata.platforms), artwork=image, theme=theme, presentation=presentation,
                           stylesheet=resources.joinpath("single_game.css").read_text(encoding="utf-8"))


def render_single_game(metadata: GameMetadata, output_path: Path,
                       artwork: Path | None = None,
                       presentation: ArtworkPresentation | None = None) -> tuple[int, int]:
    """Export a fixed 1200 × 1600 PNG; return its width and height."""
    output_path = Path(output_path)
    if output_path.suffix.lower() != ".png":
        raise RenderingError("Output path must end in .png")
    if artwork is not None and output_path.resolve() == Path(artwork).resolve():
        raise RenderingError("Output must not overwrite artwork")
    html = build_html(metadata, artwork, presentation)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page(viewport={"width": 1200, "height": 1600},
                                        device_scale_factor=1)
                page.set_default_timeout(15000)
                page.route("**/*", lambda route: route.abort())
                page.set_content(html, wait_until="load", timeout=15000)
                page.wait_for_function("document.fonts.status === 'loaded' && Array.from(document.images).every(i => i.complete)")
                decoded = artwork is None or page.evaluate("""async () => {
                    try {
                        const image = document.querySelector('figure img');
                        if (!image) return false;
                        await image.decode();
                        return image.naturalWidth > 0 && image.naturalHeight > 0;
                    } catch { return false; }
                }""")
                if not decoded:
                    raise RenderingError("Artwork could not be decoded")
                canvas = page.locator("main")
                bounds = canvas.bounding_box()
                if bounds is None:
                    raise RenderingError("Infographic layout is missing")
                fits = """() => {
                    const main = document.querySelector('main');
                    const title = main.querySelector('h1');
                    const lineHeight = parseFloat(getComputedStyle(title).lineHeight);
                    title.classList.remove('natural-wrap');
                    if (title.getBoundingClientRect().height > 2 * lineHeight + 1) {
                        title.classList.add('natural-wrap');
                    }
                    if (title.getBoundingClientRect().height > 2 * lineHeight + 1) {
                        return false;
                    }
                    const box = main.getBoundingClientRect();
                    const style = getComputedStyle(main);
                    const bottom = box.bottom - parseFloat(style.paddingBottom);
                    return main.scrollHeight <= 1600 && main.scrollWidth <= 1200 &&
                        Array.from(main.querySelectorAll('*')).every(el => {
                            if (!el.getClientRects().length) return true;
                            const r = el.getBoundingClientRect();
                            return r.bottom <= bottom + 1 && r.right <= box.right && r.left >= box.left;
                        });
                }"""
                if not page.evaluate(fits):
                    page.locator('main').evaluate("el => el.classList.add('compact')")
                if not page.evaluate(fits):
                    similar = page.locator('.similar-games-section')
                    if similar.count():
                        similar.evaluate('el => el.remove()')
                        if page.evaluate(fits):
                            logging.getLogger(__name__).warning(
                                'Similar Games omitted to fit the compact layout; input metadata is unchanged.')
                if not page.evaluate(fits):
                    raise RenderingError("Content does not fit the fixed 1200 × 1600 canvas with a maximum two-line title, even after compact layout and omitting Similar Games. No PNG was exported.")
                png = canvas.screenshot(type="png", timeout=15000)
                if png[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", png[16:24]) != (1200, 1600):
                    raise RenderingError("Chromium returned an invalid PNG or unexpected dimensions")
            finally:
                browser.close()
    except PlaywrightError as exc:
        raise RenderingError("Chromium rendering failed. Run 'python -m playwright install chromium'. " + str(exc)) from exc

    # Publish only after capture and browser cleanup succeed. A failed write or
    # replacement leaves any existing destination untouched.
    temporary = None
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=output_path.parent, prefix=".infographic-", suffix=".png", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(png)
        os.replace(temporary, output_path)
    except OSError as exc:
        raise RenderingError(f"Cannot save PNG '{output_path}': {exc}") from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return 1200, 1600
