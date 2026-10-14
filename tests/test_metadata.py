"""Exercise the research JSON contract and its nested validation."""

from datetime import date
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from game_infographic_generator.models import (
    CriticScore, GameMetadata, PlayerSentiment, Source,
)

FIXTURE = Path(__file__).parent / "fixtures" / "game_metadata.json"


def test_skill_example_matches_runtime_contract():
    skill = Path(__file__).resolve().parents[1] / "skills" / "game-research" / "SKILL.md"
    example = skill.read_text(encoding="utf-8").split("```json\n", 1)[1].split("```", 1)[0]
    data = json.loads(example)
    assert set(data) == set(GameMetadata.model_fields)
    game = GameMetadata.model_validate_json(example)
    assert json.loads(game.model_dump_json()) == data
    assert data == json.loads(FIXTURE.read_text(encoding="utf-8"))


@pytest.fixture
def metadata():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_valid_metadata(metadata):
    game = GameMetadata.model_validate(metadata)
    assert game.release_date == date(2019, 10, 31)
    assert game.alternative_titles == ["ペルソナ5 ザ・ロイヤル"]
    assert isinstance(game.critic_scores[0], CriticScore)
    assert isinstance(game.player_sentiment, PlayerSentiment)
    assert isinstance(game.sources[0], Source)
    assert GameMetadata.model_validate_json(game.model_dump_json()) == game


def test_missing_optional_fields_and_independent_defaults():
    first = GameMetadata(title="Example")
    second = GameMetadata(title="Another")
    assert first.developer is None
    assert first.publisher is None
    assert first.release_date is None
    assert first.description is None
    assert first.player_sentiment is None
    for field in ("alternative_titles", "genres", "platforms", "critic_scores",
                  "similar_games", "sources"):
        assert getattr(first, field) == []
    first.genres.append("RPG")
    assert second.genres == []
    assert PlayerSentiment().positives == []
    assert PlayerSentiment().negatives == []
    assert Source(name="Publisher").url is None


@pytest.mark.parametrize("patch", [
    {"title": 1}, {"developer": 1}, {"genres": "RPG"},
    {"platforms": [1]}, {"player_sentiment": "Positive"},
    {"critic_scores": [{"source": "Review", "score": "95", "max_score": 100,
                        "platform": "PC"}]},
    {"critic_scores": [{"source": "Review", "score": True, "max_score": 100,
                        "platform": "PC"}]},
    {"sources": [{"name": "Publisher", "url": 42}]},
])
def test_reject_incorrect_types(metadata, patch):
    metadata.update(patch)
    with pytest.raises(ValidationError):
        GameMetadata.model_validate_json(json.dumps(metadata))


@pytest.mark.parametrize("value", ["2024-02-30", "31-10-2019", "2019-10-31T00:00:00", 1572480000])
def test_reject_invalid_dates(value):
    with pytest.raises(ValidationError):
        GameMetadata.model_validate_json(json.dumps({"title": "Example", "release_date": value}))


@pytest.mark.parametrize("location", [None, "critic_scores", "player_sentiment", "sources"])
def test_reject_unexpected_fields(metadata, location):
    target = metadata if location is None else metadata[location]
    if isinstance(target, list):
        target = target[0]
    target["unexpected"] = "value"
    with pytest.raises(ValidationError, match="extra_forbidden"):
        GameMetadata.model_validate_json(json.dumps(metadata))


@pytest.mark.parametrize("field", [
    "alternative_titles", "genres", "platforms", "critic_scores", "similar_games", "sources",
])
def test_lists_are_not_nullable(field):
    with pytest.raises(ValidationError):
        GameMetadata.model_validate_json(json.dumps({"title": "Example", field: None}))


@pytest.mark.parametrize("data", [{}, {"title": ""}])
def test_title_required(data):
    with pytest.raises(ValidationError):
        GameMetadata.model_validate(data)


@pytest.mark.parametrize("score,maximum", [(-1, 100), (101, 100), (0, 0), (9.5, 10)])
def test_invalid_score_range_or_type(score, maximum):
    with pytest.raises(ValidationError):
        CriticScore(source="Review", platform="PC", score=score, max_score=maximum)
