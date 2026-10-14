"""Data models for game infographic input."""

from pydantic import BaseModel, Field


class Game(BaseModel):
    """Minimal game metadata."""

    title: str = Field(min_length=1)
