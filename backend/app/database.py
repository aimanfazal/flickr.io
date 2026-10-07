"""SQLite connection and table-creation helper."""

import pathlib

from sqlalchemy import create_engine

from .models import metadata

# Resolve the DB file relative to this file's directory so the path works
# regardless of the working directory the process is started from.
_DB_PATH = pathlib.Path(__file__).parent / "ott.db"
DATABASE_URL = f"sqlite:///{_DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_tables() -> None:
    """Create all tables defined in models.py if they don't already exist."""
    metadata.create_all(engine)
