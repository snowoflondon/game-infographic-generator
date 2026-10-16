"""Display grouping preserves platform distinctions and source metadata."""
import pytest

from game_infographic_generator.models import CriticScore, GameMetadata
from game_infographic_generator.rendering.platforms import format_platforms
from game_infographic_generator.rendering.single_game import build_html


@pytest.mark.parametrize('platforms, expected', [
    ([], ''),
    (['PC'], 'PC'),
    (['iOS', 'Android'], 'Mobile'),
    (['Android'], 'Mobile'),
    (['PlayStation 4', 'PlayStation 5'], 'PlayStation 4 & 5'),
    (['Xbox One', 'Xbox Series X|S'], 'Xbox One & Series X|S'),
    (['Nintendo Switch', 'Nintendo Switch 2'], 'Nintendo Switch & Switch 2'),
    (['Nintendo DS', 'Nintendo 3DS'], 'Nintendo DS & 3DS'),
    (['PC', 'iOS', 'PlayStation 5', 'Android', 'PlayStation 4', 'PC'],
     'PC / Mobile / PlayStation 5 & 4'),
    (['Nintendo Switch'], 'Nintendo Switch'),
    (['Wii U', 'Mystery Console', 'PC'], 'Wii U / Mystery Console / PC'),
    (['Xbox', 'Xbox One'], 'Xbox / Xbox One'),
])
def test_platform_labels(platforms, expected):
    original = platforms.copy()
    assert format_platforms(platforms) == expected
    assert platforms == original


def test_template_groups_platforms_without_changing_metadata_or_score():
    game = GameMetadata(title='Example', platforms=['PlayStation 4', 'PlayStation 5', 'iOS', 'Android'],
                        critic_scores=[CriticScore(source='Reviews', score=80, max_score=100, platform='PlayStation 5')])
    original = game.model_dump_json()
    html = build_html(game)
    assert 'PlayStation 4 &amp; 5 / Mobile' in html
    assert 'Reviews · PlayStation 5' in html
    assert game.model_dump_json() == original
