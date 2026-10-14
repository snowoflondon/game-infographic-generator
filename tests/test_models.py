import pytest
from pydantic import ValidationError

from game_infographic_generator.models import Game


def test_game_accepts_title():
    assert Game(title="Example Game").title == "Example Game"


@pytest.mark.parametrize("data", [{}, {"title": ""}, {"title": 123}])
def test_game_rejects_invalid_title(data):
    with pytest.raises(ValidationError):
        Game(**data)
