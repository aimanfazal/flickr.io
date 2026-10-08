"""GET /api/search — title search by name."""

from typing import Optional

from fastapi import APIRouter, Query
from sqlalchemy import select

from app.database import engine
from app.models import title_genres, titles
from app.routers.trends import _attach_genres
from app.schemas import SearchResult

router = APIRouter()


@router.get("/search", response_model=list[SearchResult])
def search_titles(
    q: str = Query(..., min_length=1, description="Search query (title name)"),
    platform: Optional[str] = None,
    limit: int = 20,
):
    """
    Returns titles whose name contains the query string (case-insensitive).

    Optional filters:
    - platform: Netflix | Prime | Disney+
    - limit: number of results (default 20, max 50)
    """
    limit = min(limit, 50)

    stmt = (
        select(titles)
        .where(titles.c.name.ilike(f"%{q}%"))
        .order_by(titles.c.release_year.desc())
        .limit(limit)
    )

    if platform:
        stmt = stmt.where(titles.c.platform == platform)

    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()
        title_ids = [r.id for r in rows]
        genres_map = _attach_genres(conn, title_ids)

    return [
        SearchResult(
            id=r.id,
            name=r.name,
            type=r.type,
            release_year=r.release_year,
            rating=r.rating,
            platform=r.platform,
            genres=genres_map.get(r.id, []),
            runtime_min=r.runtime_min,
            language=r.language,
            country=r.country,
            description=r.description,
            vote_count=r.vote_count,
        )
        for r in rows
    ]
