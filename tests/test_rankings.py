"""Rankings checks do not capture or generate infographic PNGs."""

from PIL import Image
import pytest
from pydantic import ValidationError

from game_infographic_generator.cli import main
from game_infographic_generator.rankings_models import RankingsInput
from game_infographic_generator.rendering.rankings import (
    LAYOUT_FITS, RankingsRenderingError, build_rankings_html, render_rankings,
)


@pytest.fixture
def ranking(tmp_path):
    Image.new('RGB', (80, 40), 'navy').save(tmp_path / 'art.jpg')
    entries = [dict(title=f'Game {10-index}', artwork_path='art.jpg') for index in range(10)]
    return RankingsInput(title='My top 10 JRPGs', games=entries)


@pytest.mark.parametrize('count', [0, 9, 11])
def test_exactly_ten(count):
    with pytest.raises(ValidationError):
        RankingsInput(title='Ranking', games=[dict(title='Game', artwork_path='a.jpg')]*count)


def test_schema_rejects_drift_and_blank_values(ranking):
    for mutate in [lambda d:d.update(extra=True), lambda d:d.update(title=' '),
                   lambda d:d['games'][0].update(rank=10),
                   lambda d:d['games'][0].update(title=' '),
                   lambda d:d['games'][0].update(artwork_path=4),
                   lambda d:d['games'][0].update(title=7),
                   lambda d:d['games'][0].update(metadata_path='old.json'),
                   lambda d:d['games'][0].update(alternative_titles=['Removed'])]:
        data=ranking.model_dump();mutate(data)
        with pytest.raises(ValidationError):RankingsInput.model_validate(data)


def test_order_content_escaping_and_no_mutation(ranking, tmp_path):
    ranking.games[0].title='<script>日本語 中文 한국어 & Game</script>'
    before=ranking.model_dump_json()
    html=build_rankings_html(ranking,tmp_path)
    assert html.count('class="ranking-row"')==10
    assert html.index('&lt;script&gt;日本語 中文 한국어 &amp; Game&lt;/script&gt;') < html.index('<h2>Game 9</h2>') < html.index('<h2>Game 1</h2>')
    assert '<script>' not in html and '日本語 中文 한국어 &amp; Game' in html
    assert 'class="alternative"' not in html
    assert not list(tmp_path.glob('game-*.json'))
    assert ranking.model_dump_json()==before


@pytest.mark.parametrize('broken', ['artwork', 'corrupt'])
def test_bad_input_preserves_output(ranking,tmp_path,broken):
    output=tmp_path/'result.png';output.write_bytes(b'existing output')
    if broken=='artwork':(tmp_path/'art.jpg').unlink()
    elif broken=='corrupt':(tmp_path/'art.jpg').write_bytes(b'not an image')
    with pytest.raises(RankingsRenderingError,match='Rank 1'):
        render_rankings(ranking,output,tmp_path)
    assert output.read_bytes()==b'existing output'


def test_cli_check_relative_paths_no_browser(ranking,tmp_path,monkeypatch,capsys):
    import game_infographic_generator.rendering.rankings as module
    def forbidden():raise AssertionError('Check must not launch browser')
    monkeypatch.setattr(module,'sync_playwright',forbidden)
    manifest=tmp_path/'ranking.json';manifest.write_text(ranking.model_dump_json())
    output=tmp_path/'result.png'
    assert main(['rankings',str(manifest),str(output),'--check'])==0
    assert not output.exists() and 'no PNG exported' in capsys.readouterr().out
    assert main(['rankings',str(manifest),str(manifest),'--check'])==1
    assert main(['rankings',str(manifest),str(tmp_path/'art.jpg'),'--check'])==1


def test_cli_dispatch(ranking,tmp_path,monkeypatch):
    import game_infographic_generator.rendering.rankings as module
    seen=[]
    def render(value,output,base):
        seen.append((value,output,base));return 1200,1600
    monkeypatch.setattr(module,'render_rankings',render)
    manifest=tmp_path/'ranking.json';manifest.write_text(ranking.model_dump_json())
    assert main(['rankings',str(manifest),str(tmp_path/'out.png')])==0
    assert seen[0][0]==ranking and seen[0][2]==tmp_path


def test_real_browser_layout_without_screenshots(ranking,tmp_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True)
        try:
            page=browser.new_page(viewport={'width':1200,'height':1600})
            page.set_content(build_rankings_html(ranking,tmp_path))
            page.evaluate('document.fonts.ready')
            assert page.evaluate(LAYOUT_FITS)
            assert page.locator('.ranking-row h2').all_text_contents()==[f'Game {10-i}' for i in range(10)]
            heights=page.locator('.ranking-row').evaluate_all('els => els.map(e => e.getBoundingClientRect().height)')
            assert max(heights)-min(heights)<1
            page.locator('.ranking-row h2').first.evaluate("el => el.textContent = 'Very long title '.repeat(70)")
            assert not page.evaluate(LAYOUT_FITS)
        finally:browser.close()


def test_browser_failure_preserves_output_without_capture(ranking,tmp_path,monkeypatch):
    import game_infographic_generator.rendering.rankings as module
    from playwright.sync_api import Error
    def fail():raise Error('Browser unavailable')
    monkeypatch.setattr(module,'sync_playwright',fail)
    output=tmp_path/'result.png';output.write_bytes(b'previous output')
    with pytest.raises(RankingsRenderingError,match='Chromium rendering failed'):
        render_rankings(ranking,output,tmp_path)
    assert output.read_bytes()==b'previous output'


def test_output_cannot_replace_an_image_input(ranking,tmp_path):
    image=tmp_path/'protected.png'
    image.write_bytes((tmp_path/'art.jpg').read_bytes())
    ranking.games[0].artwork_path='protected.png'
    before=image.read_bytes()
    with pytest.raises(RankingsRenderingError,match='overwrite'):
        render_rankings(ranking,image,tmp_path)
    assert image.read_bytes()==before


@pytest.mark.parametrize('title', ['Series: Subtitle', 'Series:Subtitle', 'シリーズ：サブタイトル', 'Title:', '<script>: A & B'])
def test_colon_hints_preserve_title_text(ranking,tmp_path,title):
    from html.parser import HTMLParser
    class Reader(HTMLParser):
        def __init__(self):super().__init__();self.active=False;self.parts=[]
        def handle_starttag(self,tag,attrs):
            if tag=='h2' and not self.parts:self.active=True
        def handle_endtag(self,tag):
            if tag=='h2':self.active=False
        def handle_data(self,data):
            if self.active:self.parts.append(data)
    ranking.games[0].title=title
    html=build_rankings_html(ranking,tmp_path);reader=Reader();reader.feed(html)
    assert ''.join(reader.parts)==title
    assert '<script>' not in html


def test_browser_colon_preference_and_natural_fallback(ranking,tmp_path):
    from playwright.sync_api import sync_playwright
    ranking.title='Personal: Rankings'
    ranking.games[0].title='Series Series: Adventure Adventure Adventure'
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True)
        try:
            page=browser.new_page(viewport={'width':1200,'height':1600})
            page.set_content(build_rankings_html(ranking,tmp_path));page.evaluate('document.fonts.ready')
            title=page.locator('h2').first
            # Find a real font-measured width where colon grouping costs a third
            # line but natural wrapping uses two. No screenshot is captured.
            width=title.evaluate('''el => {
                const line=parseFloat(getComputedStyle(el).lineHeight);
                for(let w=250;w<=550;w+=10) {
                    el.style.width=w+'px'; el.classList.remove('natural-wrap');
                    const grouped=el.getBoundingClientRect().height;
                    el.classList.add('natural-wrap');
                    const natural=el.getBoundingClientRect().height;
                    if(grouped>2*line+1 && natural<=2*line+1) return w;
                }
                return null;
            }''')
            assert width is not None
            assert page.evaluate(LAYOUT_FITS)
            assert 'natural-wrap' in title.get_attribute('class')
            assert 'natural-wrap' not in (page.locator('h1').get_attribute('class') or '')
            assert title.text_content()==ranking.games[0].title
            title.evaluate("el => el.style.width='100px'")
            assert not page.evaluate(LAYOUT_FITS)
        finally:browser.close()


def test_bottom_left_titles_with_left_half_gradient(ranking,tmp_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True)
        try:
            page=browser.new_page(viewport={'width':1200,'height':1600})
            page.set_content(build_rankings_html(ranking,tmp_path));page.evaluate('document.fonts.ready')
            assert page.evaluate(LAYOUT_FITS)
            assert page.locator('.rank').count()==0
            assert page.locator('.shade').count()==10
            assert page.locator('h1').evaluate("el => getComputedStyle(el).textTransform")== 'none'
            assert page.locator('.ranking-row').evaluate_all('''rows => rows.every(row => {
                const r=row.getBoundingClientRect(), t=row.querySelector('.row-copy').getBoundingClientRect();
                const image=getComputedStyle(row.querySelector('img'));
                return Math.abs(t.left-r.left-32)<1 && Math.abs(r.bottom-t.bottom-12)<1 &&
                    t.right<=r.left+r.width/2+1 && t.height<r.height && image.filter==='none' && image.opacity==='1';
            })''')
        finally:browser.close()


@pytest.mark.parametrize('focal', [{'x':-1}, {'y':101}, {'x':'50'}, {'y':float('nan')}, {'x':True}, {'z':50}])
def test_invalid_focal_points(ranking,focal):
    data=ranking.model_dump();data['games'][0]['artwork_focal_point']=focal
    with pytest.raises(ValidationError):RankingsInput.model_validate(data)


def test_focal_points_are_embedded_without_changing_input(ranking,tmp_path):
    ranking.games[0].artwork_focal_point.y=20
    before=ranking.model_dump_json()
    html=build_rankings_html(ranking,tmp_path)
    assert 'object-position: 50.0% 20%' in html
    assert ranking.model_dump_json()==before


def test_light_palette_frame_and_rounded_cards(ranking,tmp_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True)
        try:
            page=browser.new_page(viewport={'width':1200,'height':1600})
            page.set_content(build_rankings_html(ranking,tmp_path));page.evaluate('document.fonts.ready')
            assert page.evaluate(LAYOUT_FITS)
            assert page.locator('main').evaluate("el => getComputedStyle(el).backgroundColor")=='rgb(245, 243, 237)'
            assert page.locator('h1').evaluate("el => getComputedStyle(el).color")=='rgb(37, 43, 43)'
            assert page.locator('footer').evaluate("el => getComputedStyle(el).color")=='rgb(93, 105, 105)'
            assert page.locator('.rankings').evaluate('''el => {
                const r=el.getBoundingClientRect(), s=getComputedStyle(el);
                return r.left===48 && r.right===1152 && s.rowGap==='6px' && s.backgroundColor==='rgba(0, 0, 0, 0)';
            }''')
            assert page.locator('.ranking-row').evaluate_all('''rows => rows.every((el,i) => {
                const s=getComputedStyle(el), r=el.getBoundingClientRect();
                const next=rows[i+1]?.getBoundingClientRect();
                return ['borderTopLeftRadius','borderTopRightRadius','borderBottomLeftRadius','borderBottomRightRadius'].every(k=>s[k]==='8px') &&
                    s.overflow==='hidden' && s.boxShadow==='none' && s.borderTopWidth==='0px' &&
                    s.backgroundColor==='rgba(0, 0, 0, 0)' && (!next || Math.abs(next.top-r.bottom-6)<1);
            })''')
        finally:browser.close()


def test_softened_gradient_white_text_contrast():
    # Weakest shade under text is 64% black; pure white art is the worst case.
    channel=1-.64
    linear=((channel+.055)/1.055)**2.4
    assert 1.05/(linear+.05)>=4.5
