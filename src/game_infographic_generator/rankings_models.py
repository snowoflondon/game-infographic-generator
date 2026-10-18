"""Personal ranking order and local inputs, separate from game research."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ArtworkFocalPoint(BaseModel):
    """CSS object-position percentages; 0 is left/top and 100 right/bottom."""

    model_config = ConfigDict(extra='forbid', strict=True)
    x: float = Field(default=50.0, ge=0, le=100, allow_inf_nan=False)
    y: float = Field(default=50.0, ge=0, le=100, allow_inf_nan=False)


class RankingEntry(BaseModel):
    """References resolve relative to the containing manifest."""

    model_config = ConfigDict(extra='forbid', strict=True)
    title: str = Field(min_length=1)
    artwork_path: str = Field(min_length=1)
    artwork_focal_point: ArtworkFocalPoint = Field(default_factory=ArtworkFocalPoint)

    @field_validator('title', 'artwork_path')
    @classmethod
    def nonblank_value(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('title and artwork path must not be blank')
        return value


class RankingsInput(BaseModel):
    """The first entry is #1; never sort, deduplicate or infer order."""

    model_config = ConfigDict(extra='forbid', strict=True)
    title: str = Field(min_length=1)
    games: list[RankingEntry] = Field(min_length=10, max_length=10)

    @field_validator('title')
    @classmethod
    def nonblank_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('title must not be blank')
        return value
