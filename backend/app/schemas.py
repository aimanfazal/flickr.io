"""Pydantic response models for all API endpoints."""

from typing import Optional
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# /api/ratings
# ---------------------------------------------------------------------------

class RatingCount(BaseModel):
    rating: str
    count: int


# ---------------------------------------------------------------------------
# /api/genres
# ---------------------------------------------------------------------------

class GenreCount(BaseModel):
    genre: str
    count: int


# ---------------------------------------------------------------------------
# /api/releases
# ---------------------------------------------------------------------------

class ReleaseCount(BaseModel):
    release_year: int
    count: int


# ---------------------------------------------------------------------------
# /api/trends
# ---------------------------------------------------------------------------

class TrendTitle(BaseModel):
    id: int
    name: str
    type: Optional[str]
    release_year: Optional[int]
    rating: Optional[str]
    runtime_min: Optional[int]
    platform: Optional[str]
    genres: list[str]


# ---------------------------------------------------------------------------
# /api/search
# ---------------------------------------------------------------------------

class SearchResult(BaseModel):
    id: int
    name: str
    type: Optional[str]
    release_year: Optional[int]
    rating: Optional[str]
    platform: Optional[str]
    genres: list[str]
