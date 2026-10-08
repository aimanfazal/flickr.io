"""SQLite connection and table-creation helper."""

import pathlib

from sqlalchemy import create_engine, select

from .models import metadata, users

# Resolve the DB file relative to this file's directory so the path works
# regardless of the working directory the process is started from.
_DB_PATH = pathlib.Path(__file__).parent / "ott.db"
DATABASE_URL = f"sqlite:///{_DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_tables() -> None:
    """Create all tables defined in models.py if they don't already exist."""
    metadata.create_all(engine)
    _seed_demo_user()


def _seed_demo_user() -> None:
    """Insert a demo user if the users table is empty."""
    import bcrypt as _bcrypt  # imported here to keep startup fast
    with engine.connect() as conn:
        row = conn.execute(select(users).where(users.c.username == "admin")).first()
        if row is None:
            hashed = _bcrypt.hashpw(b"password", _bcrypt.gensalt()).decode()
            conn.execute(users.insert().values(
                username="admin",
                hashed_password=hashed,
                is_active=True,
            ))
            conn.commit()
