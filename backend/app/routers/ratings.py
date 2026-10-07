"""GET /api/ratings — content rating distribution."""

from typing import Optional

from fastapi import APIRouter
from sqlalchemy import func, select

from app.database import engine
from app.models import titles
from app.schemas import RatingCount

router = APIRouter()


@router.get("/ratings", response_model=list[RatingCount])
def get_ratings(
    platform: Optional[str] = None,
    type: Optional[str] = None,
):
    """
    Returns the count of titles grouped by content rating (PG, TV-MA, R, …).

    Optional filters:
    - platform: Netflix | Prime | Disney+
    - type: Movie | TV Show
    """
    stmt = (
        select(titles.c.rating, func.count().label("count"))
        .where(titles.c.rating.isnot(None))
        .group_by(titles.c.rating)
        .order_by(func.count().desc())
    )

    if platform:
        stmt = stmt.where(titles.c.platform == platform)
    if type:
        stmt = stmt.where(titles.c.type == type)

    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()

    return [RatingCount(rating=r[0], count=r[1]) for r in rows]
