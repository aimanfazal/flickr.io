"""GET /api/releases — title counts grouped by release year."""

from typing import Optional

from fastapi import APIRouter
from sqlalchemy import func, select

from app.database import engine
from app.models import titles
from app.schemas import ReleaseCount

router = APIRouter()


@router.get("/releases", response_model=list[ReleaseCount])
def get_releases(
    platform: Optional[str] = None,
    type: Optional[str] = None,
):
    """
    Returns the number of titles released per year, ascending.

    Optional filters:
    - platform: Netflix | Prime | Disney+
    - type: Movie | TV Show
    """
    stmt = (
        select(titles.c.release_year, func.count().label("count"))
        .where(titles.c.release_year.isnot(None))
        .group_by(titles.c.release_year)
        .order_by(titles.c.release_year.asc())
    )

    if platform:
        stmt = stmt.where(titles.c.platform == platform)
    if type:
        stmt = stmt.where(titles.c.type == type)

    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()

    return [ReleaseCount(release_year=r[0], count=r[1]) for r in rows]
