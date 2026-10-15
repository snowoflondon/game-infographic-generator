"""Template behavior and actual Chromium capture."""
import struct
from pathlib import Path

import pytest
from game_infographic_generator.models import GameMetadata, PlayerSentiment
from game_infographic_generator.rendering.single_game import build_html as raw_html, render_single_game as raw_render, RenderingError
from game_infographic_generator.rendering.presentation import ArtworkPresentation


def copy_for(game):
    sentiment = game.player_sentiment
    return ArtworkPresentation(overview='A brief overview.' if game.description else None,
        highlights=['Positive theme'] if sentiment and sentiment.positives else [],
        criticisms=['Critical theme'] if sentiment and sentiment.negatives else [])


def build_html(game, artwork=None):
    return raw_html(game, artwork, copy_for(game) if artwork else None)


def render_single_game(game, output, artwork=None):
    return raw_render(game, output, artwork, copy_for(game) if artwork else None)



@pytest.fixture
def artwork(tmp_path):
    import base64
    path = tmp_path / 'art.png'
    path.write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a2ioAAAAASUVORK5CYII='))
    return path


def test_sparse_and_escaped(artwork):
    html = build_html(GameMetadata(title='<script>bad()</script>', player_sentiment=PlayerSentiment()), artwork)
    assert '&lt;script&gt;' in html
    assert '<script>' not in html
    assert '<section>' not in html
    assert '<figure>' in html
    assert 'None' not in html


def test_unicode_and_scores(artwork):
    game = GameMetadata.model_validate_json((Path(__file__).parent / 'fixtures/game_metadata.json').read_text())
    html = build_html(game, artwork)
    assert game.alternative_titles[0] in html
    assert '95' in html and '100' in html
    assert 'PlayStation 4' in html


def test_invalid_artwork(tmp_path):
    with pytest.raises(RenderingError):
        build_html(GameMetadata(title='Title'), tmp_path / 'image.svg')


def test_actual_png(tmp_path, artwork):
    image = artwork
    output = tmp_path / 'result.png'
    game = GameMetadata(title='Long title 原神 ペルソナ 스텔라 ' * 2, description='Readable text. ' * 10)
    width, height = render_single_game(game, output, image)
    data = output.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    assert struct.unpack('>II', data[16:24]) == (width, height)
    assert (width, height) == (1200, 1600)


def test_sources_omitted_without_mutation(artwork):
    from game_infographic_generator.models import Source, CriticScore
    game = GameMetadata(title='Example', sources=[Source(name='Hidden source', url='https://example.com')],
                        critic_scores=[CriticScore(source='Aggregator', score=80, max_score=100, platform='PC', url='https://review.example.com')])
    before = game.model_dump_json()
    html = build_html(game, artwork)
    assert 'Hidden source' not in html
    assert 'https://' not in html
    assert 'Aggregator' in html
    assert game.model_dump_json() == before


def test_overflow_rejected(tmp_path, artwork):
    output = tmp_path / 'overflow.png'
    with pytest.raises(RenderingError, match='does not fit'):
        render_single_game(GameMetadata(title='Very long title ' * 500), output, artwork)
    assert not output.exists()


def test_genshin_with_artwork_uses_condensed_copy(tmp_path, artwork):
    source = Path(__file__).resolve().parents[1] / 'data/validation-runs/genshin_impact__2026-10-14T192010-0400__game-research.json'
    original = source.read_bytes()
    game = GameMetadata.model_validate_json(original)
    assert render_single_game(game, tmp_path / 'genshin.png', artwork) == (1200, 1600)
    assert source.read_bytes() == original


def test_artwork_requires_presentation(artwork):
    with pytest.raises(RenderingError, match='condensed copy'):
        raw_html(GameMetadata(title='Example'), artwork)


def test_corrupt_artwork_fails(tmp_path):
    artwork = tmp_path / 'broken.png'
    artwork.write_bytes(b'not an image')
    with pytest.raises(RenderingError, match='decoded'):
        render_single_game(GameMetadata(title='Example'), tmp_path / 'result.png', artwork)
    assert not (tmp_path / 'result.png').exists()


@pytest.mark.parametrize('failure', ['missing', 'corrupt', 'undecodable', 'overflow', 'browser', 'capture', 'write'])
def test_failure_preserves_existing_png(tmp_path, artwork, monkeypatch, failure):
    from game_infographic_generator.rendering import single_game
    from playwright.sync_api import BrowserType, Locator, Error
    output = tmp_path / 'existing.png'
    original = artwork.read_bytes()
    output.write_bytes(original)
    game = GameMetadata(title='Example')
    if failure == 'missing':
        artwork = tmp_path / 'missing.png'
    elif failure == 'corrupt':
        artwork.write_bytes(b'bad')
    elif failure == 'undecodable':
        artwork.write_bytes(b'\x89PNG\r\n\x1a\n' + b'broken payload')
    elif failure == 'overflow':
        game = GameMetadata(title='Too long ' * 1000)
    elif failure == 'browser':
        def fail(*args, **kwargs):
            raise Error('Cannot launch browser')
        monkeypatch.setattr(BrowserType, 'launch', fail)
    elif failure == 'capture':
        def fail(*args, **kwargs):
            raise Error('Capture failed')
        monkeypatch.setattr(Locator, 'screenshot', fail)
    elif failure == 'write':
        def fail(*args, **kwargs):
            raise OSError('Replacement denied')
        monkeypatch.setattr(single_game.os, 'replace', fail)
    with pytest.raises(RenderingError):
        render_single_game(game, output, artwork)
    assert output.read_bytes() == original
    assert not list(tmp_path.glob('.infographic-*.png'))


def test_compact_retains_artwork(tmp_path, artwork, monkeypatch):
    from playwright.sync_api import Locator
    capture = Locator.screenshot
    observed = {}
    def inspect(self, *args, **kwargs):
        observed.update(self.evaluate('''el => {
            const figure = el.querySelector('figure');
            const rect = figure.getBoundingClientRect();
            return {compact: el.classList.contains('compact'), ratio: rect.width / rect.height,
                    loaded: figure.querySelector('img').naturalWidth > 0};
        }'''))
        return capture(self, *args, **kwargs)
    monkeypatch.setattr(Locator, 'screenshot', inspect)
    game = GameMetadata(title='Long title ' * 35, description='A readable sentence. ' * 65)
    assert render_single_game(game, tmp_path / 'compact.png', artwork) == (1200, 1600)
    assert observed['compact']
    assert observed['loaded']
    assert observed['ratio'] == pytest.approx(16 / 9)


def test_theme_variables_and_unmodified_artwork(artwork):
    original = artwork.read_bytes()
    html = build_html(GameMetadata(title='Theme test'), artwork)
    assert '--accent:' in html
    assert '--on-accent:' in html
    assert '--background: #f5f3ee' in html
    import base64
    assert base64.b64encode(original).decode('ascii') in html
    assert artwork.read_bytes() == original


def test_full_mode_preserves_source_text():
    game = GameMetadata(title='Example', description='First sentence. Second sentence.',
        player_sentiment=PlayerSentiment(summary='Mixed views.', positives=['Detailed praise'], negatives=['Detailed criticism']))
    html = raw_html(game)
    assert game.description in html and 'Mixed views.' in html
    assert '<figure>' not in html
    assert 'Detailed praise' in html


def test_artwork_copy_is_separate(artwork):
    game = GameMetadata(title='Example', description='First sentence. Second sentence.',
        player_sentiment=PlayerSentiment(summary='Mixed opinions.', positives=['Some praise exploration.'], negatives=['Some dislike pacing.']))
    before = game.model_dump_json()
    copy = ArtworkPresentation(overview='An exploratory adventure.', highlights=['Exploration'], criticisms=['Pacing'])
    html = raw_html(game, artwork, copy)
    assert copy.overview in html
    assert game.description not in html and 'Mixed opinions.' not in html
    assert 'Highlights' in html and 'Criticisms' in html
    assert 'Exploration' in html and 'Pacing' in html
    assert game.model_dump_json() == before


def test_presentation_rejects_invalid_copy():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        ArtworkPresentation(overview='First sentence. Second sentence.')
    with pytest.raises(ValidationError):
        ArtworkPresentation(highlights=[''])


def test_full_mode_real_png(tmp_path):
    assert raw_render(GameMetadata(title='Typography only'), tmp_path / 'plain.png') == (1200, 1600)
