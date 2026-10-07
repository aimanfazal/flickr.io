"""GET /api/trends — most recent titles, optionally filtered."""

from typing import Optional

from fastapi import APIRouter
from sqlalchemy import select

from app.database import engine
from app.models import title_genres, titles
from app.schemas import TrendTitle

router = APIRouter()


def _attach_genres(conn, title_ids: list[int]) -> dict[int, list[str]]:
    """Return a mapping of title_id → [genre, …] for the given IDs."""
    if not title_ids:
        return {}
    rows = conn.execute(
        select(title_genres.c.title_id, title_genres.c.genre).where(
            title_genres.c.title_id.in_(title_ids)
        )
    ).fetchall()
    result: dict[int, list[str]] = {tid: [] for tid in title_ids}
    for tid, genre in rows:
        result[tid].append(genre)
    return result


@router.get("/trends", response_model=list[TrendTitle])
def get_trends(
    platform: Optional[str] = None,
    genre: Optional[str] = None,
    limit: int = 20,
):
    """
    Returns the most recently released titles (sorted by release_year DESC).

    Optional filters:
    - platform: Netflix | Prime | Disney+
    - genre: exact genre label (e.g. "Dramas")
    - limit: number of results (default 20, max 100)
    """
    limit = min(limit, 100)

    stmt = (
        select(titles)
        .where(titles.c.release_year.isnot(None))
        .order_by(titles.c.release_year.desc())
        .limit(limit)
    )

    if platform:
        stmt = stmt.where(titles.c.platform == platform)

    if genre:
        # Semi-join: only titles that have this genre
        genre_subq = (
            select(title_genres.c.title_id)
            .where(title_genres.c.genre == genre)
            .scalar_subquery()
        )
        stmt = stmt.where(titles.c.id.in_(genre_subq))

    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()
        title_ids = [r.id for r in rows]
        genres_map = _attach_genres(conn, title_ids)

    return [
        TrendTitle(
            id=r.id,
            name=r.name,
            type=r.type,
            release_year=r.release_year,
            rating=r.rating,
            runtime_min=r.runtime_min,
            platform=r.platform,
            genres=genres_map.get(r.id, []),
        )
        for r in rows
    ]
