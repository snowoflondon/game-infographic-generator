"""Structured game metadata shared by research and rendering."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class MetadataModel(BaseModel):
    """Reject schema drift and implicit type coercion."""

    model_config = ConfigDict(extra="forbid", strict=True)


class Game(MetadataModel):
    """Minimal game identity."""

    title: str = Field(min_length=1)


class CriticScore(MetadataModel):
    """A score on its original scale for a specific platform."""

    source: str = Field(min_length=1)
    score: int = Field(ge=0)
    max_score: int = Field(gt=0)
    platform: str = Field(min_length=1)
    url: Optional[str] = None

    @model_validator(mode="after")
    def check_score_range(self) -> "CriticScore":
        if self.score > self.max_score:
            raise ValueError("score must not exceed max_score")
        return self


class PlayerSentiment(MetadataModel):
    """Community opinions, distinct from factual metadata."""

    summary: Optional[str] = None
    positives: list[str] = Field(default_factory=list)
    negatives: list[str] = Field(default_factory=list)


class Source(MetadataModel):
    """A reference supporting researched claims."""

    name: str = Field(min_length=1)
    url: Optional[str] = None


class GameMetadata(Game):
    """Research contract for one game edition; only its title is required."""

    alternative_titles: list[str] = Field(default_factory=list)
    developer: Optional[str] = None
    publisher: Optional[str] = None
    release_date: Optional[date] = None
    genres: list[str] = Field(default_factory=list)
    platforms: list[str] = Field(default_factory=list)
    description: Optional[str] = None
    critic_scores: list[CriticScore] = Field(default_factory=list)
    player_sentiment: Optional[PlayerSentiment] = None
    similar_games: list[str] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)

    @field_validator("release_date", mode="before")
    @classmethod
    def parse_release_date(cls, value: object) -> object:
        if isinstance(value, str):
            parsed = date.fromisoformat(value)
            if parsed.isoformat() != value:
                raise ValueError("release_date must use YYYY-MM-DD")
            return parsed
        return value
