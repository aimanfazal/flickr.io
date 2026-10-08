"""SQLAlchemy Core table definitions."""

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    Table,
    Text,
    UniqueConstraint,
)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", Text, nullable=False, unique=True),
    Column("hashed_password", Text, nullable=False),
    Column("is_active", Boolean, default=True),
)

titles = Table(
    "titles",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", Text, nullable=False),
    Column("type", Text),                   # "Movie" or "TV Show"
    Column("release_year", Integer),
    Column("rating", Text),                 # Content/age rating (PG, TV-MA, …)
    Column("vote_count", Integer),          # NULL until a numeric source is added
    Column("runtime_min", Integer),         # NULL for TV Shows
    Column("language", Text),
    Column("country", Text),
    Column("platform", Text),               # "Netflix" | "Prime" | "Disney+"
    Column("description", Text),
    UniqueConstraint("name", "release_year", "platform", name="uq_title_year_platform"),
)

title_genres = Table(
    "title_genres",
    metadata,
    Column("title_id", Integer, ForeignKey("titles.id"), nullable=False),
    Column("genre", Text, nullable=False),
    UniqueConstraint("title_id", "genre", name="uq_title_genre"),
)
