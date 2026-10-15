"""Separate, agent-authored copy for artwork mode; never research metadata."""

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ArtworkPresentation(BaseModel):
    """Faithful one-sentence overview and short sentiment phrases."""

    model_config = ConfigDict(extra='forbid', strict=True)
    overview: str | None = Field(default=None, max_length=400)
    highlights: list[str] = Field(default_factory=list)
    criticisms: list[str] = Field(default_factory=list)

    @field_validator('overview')
    @classmethod
    def concise_overview(cls, value: str | None) -> str | None:
        if value is not None and (not value.strip() or '\n' in value or len(re.split(r'[.!?。！？]+\s+|[。！？]', value.strip().rstrip('.!?。！？'))) > 1):
            raise ValueError('overview must be one nonempty sentence')
        return value

    @field_validator('highlights', 'criticisms')
    @classmethod
    def short_points(cls, values: list[str]) -> list[str]:
        if any(not value.strip() or len(value) > 100 or '\n' in value for value in values):
            raise ValueError('sentiment points must be short, nonempty phrases (up to 100 characters)')
        return values
