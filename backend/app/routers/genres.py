"""GET /api/genres — genre distribution."""

from typing import Optional

from fastapi import APIRouter
from sqlalchemy import func, select

from app.database import engine
from app.models import title_genres, titles
from app.schemas import GenreCount

router = APIRouter()


@router.get("/genres", response_model=list[GenreCount])
def get_genres(
    platform: Optional[str] = None,
    release_year: Optional[int] = None,
):
    """
    Returns the count of titles per genre, descending.

    Optional filters:
    - platform: Netflix | Prime | Disney+
    - release_year: e.g. 2022
    """
    stmt = (
        select(title_genres.c.genre, func.count().label("count"))
        .select_from(title_genres.join(titles, title_genres.c.title_id == titles.c.id))
        .group_by(title_genres.c.genre)
        .order_by(func.count().desc())
    )

    if platform:
        stmt = stmt.where(titles.c.platform == platform)
    if release_year:
        stmt = stmt.where(titles.c.release_year == release_year)

    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()

    return [GenreCount(genre=r[0], count=r[1]) for r in rows]
