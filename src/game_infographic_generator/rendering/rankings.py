"""Independent ten-game rankings layout using supplied titles and verified artwork."""

import base64
from importlib.resources import files
import os
from pathlib import Path
import struct
import tempfile

from jinja2 import Environment, StrictUndefined
from PIL import Image
from playwright.sync_api import Error as PlaywrightError, sync_playwright

from ..rankings_models import RankingsInput


class RankingsRenderingError(RuntimeError):
    """A rankings input or layout could not be rendered."""


def input_paths(ranking: RankingsInput, base_dir: Path) -> list[Path]:
    """Return all referenced input paths, retaining the supplied order."""
    return [(base_dir / entry.artwork_path).resolve() for entry in ranking.games]


def build_rankings_html(ranking: RankingsInput, base_dir: Path) -> str:
    """Embed decoded artwork alongside supplied titles; never sort."""
    rows = []
    for rank, entry in enumerate(ranking.games, 1):
        artwork_path = base_dir / entry.artwork_path
        try:
            data = artwork_path.read_bytes()
            with Image.open(artwork_path) as image:
                image.load()
                mime = {'PNG': 'image/png', 'JPEG': 'image/jpeg', 'WEBP': 'image/webp'}.get(image.format)
                if mime is None or min(image.size) <= 0:
                    raise ValueError('artwork must be a decodable PNG, JPEG or WebP')
        except (OSError, ValueError, UnicodeError) as exc:
            raise RankingsRenderingError(f'Rank {rank}: cannot load artwork: {exc}') from exc
        rows.append(dict(title=entry.title, focal=entry.artwork_focal_point,
                         artwork=f'data:{mime};base64,' + base64.b64encode(data).decode('ascii')))
    resources = files(__package__).joinpath('templates')
    env = Environment(autoescape=True, undefined=StrictUndefined)
    return env.from_string(resources.joinpath('rankings.html.j2').read_text(encoding='utf-8')).render(
        title=ranking.title, rows=rows, stylesheet=resources.joinpath('rankings.css').read_text(encoding='utf-8'))


# Measure real text after fonts load; do not hide, clamp or truncate overflowing copy.
LAYOUT_FITS = """() => {
    const main = document.querySelector('main');
    for (const title of main.querySelectorAll('h1, h2')) {
        title.classList.remove('natural-wrap');
        const lineHeight = parseFloat(getComputedStyle(title).lineHeight);
        if (title.getBoundingClientRect().height > 2 * lineHeight + 1) {
            title.classList.add('natural-wrap');
        }
    }
    const box = main.getBoundingClientRect();
    const rows = [...document.querySelectorAll('.ranking-row')];
    const titleFits = el => el.getBoundingClientRect().height <=
        2 * parseFloat(getComputedStyle(el).lineHeight) + 1;
    return rows.length === 10 && titleFits(document.querySelector('h1')) &&
        rows.every(row => {
            const text = row.querySelector('.row-copy');
            const r = row.getBoundingClientRect(), t = text.getBoundingClientRect();
            return titleFits(row.querySelector('h2')) && t.top >= r.top && t.bottom <= r.bottom &&
                t.right <= r.left + r.width / 2 + 1 &&
                Math.abs(r.height - rows[0].getBoundingClientRect().height) < 1;
        }) && [...main.querySelectorAll('header, footer, .row-copy, h1, h2')].every(el => {
            const r = el.getBoundingClientRect();
            return r.left >= box.left && r.right <= box.right && r.top >= box.top &&
                r.bottom <= box.bottom && el.scrollWidth <= el.clientWidth + 1 &&
                el.scrollHeight <= el.clientHeight + 1;
        }) && main.scrollHeight <= 1600 && main.scrollWidth <= 1200;
}"""


def render_rankings(ranking: RankingsInput, output_path: Path, base_dir: Path) -> tuple[int, int]:
    """Export ten equal artwork bands, preserving existing output on failure."""
    output_path = Path(output_path)
    if output_path.suffix.lower() != '.png':
        raise RankingsRenderingError('Output path must end in .png')
    if output_path.resolve() in input_paths(ranking, base_dir):
        raise RankingsRenderingError('Output must not overwrite artwork')
    html = build_rankings_html(ranking, base_dir)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page(viewport={'width': 1200, 'height': 1600}, device_scale_factor=1)
                page.set_default_timeout(15000)
                page.route('**/*', lambda route: route.abort())
                page.set_content(html, wait_until='load', timeout=15000)
                page.wait_for_function("document.fonts.status === 'loaded' && [...document.images].every(i => i.complete)")
                if not page.evaluate("async () => { try { await Promise.all([...document.images].map(i => i.decode())); return [...document.images].every(i => i.naturalWidth > 0); } catch { return false; } }"):
                    raise RankingsRenderingError('A ranking artwork image could not be decoded')
                if not page.evaluate(LAYOUT_FITS):
                    raise RankingsRenderingError('Rankings text does not fit ten equal stripes with two-line titles; no PNG exported')
                png = page.locator('main').screenshot(type='png', timeout=15000)
                if png[:8] != b'\x89PNG\r\n\x1a\n' or struct.unpack('>II', png[16:24]) != (1200, 1600):
                    raise RankingsRenderingError('Chromium returned an invalid PNG or dimensions')
            finally:
                browser.close()
    except PlaywrightError as exc:
        raise RankingsRenderingError("Chromium rendering failed; run 'python -m playwright install chromium'. " + str(exc)) from exc
    temporary = None
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=output_path.parent, prefix='.rankings-', suffix='.png', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(png)
        os.replace(temporary, output_path)
    except OSError as exc:
        raise RankingsRenderingError(f'Cannot save rankings PNG: {exc}') from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return 1200, 1600
