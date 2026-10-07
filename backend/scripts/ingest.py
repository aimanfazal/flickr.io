"""
Ingest a Kaggle OTT CSV into the local SQLite database.

Usage:
    python -m scripts.ingest --platform netflix
    python -m scripts.ingest --platform prime
    python -m scripts.ingest --platform disney
"""

import argparse
import pathlib
import sys

import pandas as pd
from sqlalchemy import select, text

# Allow running as `python scripts/ingest.py` from the backend/ directory.
_BACKEND_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BACKEND_DIR))

from app.database import create_tables, engine  # noqa: E402
from app.models import title_genres, titles  # noqa: E402

# ---------------------------------------------------------------------------
# Platform configuration
# ---------------------------------------------------------------------------
PLATFORM_MAP = {
    "netflix": {
        "filename": "netflix_titles.csv",
        "label": "Netflix",
    },
    "prime": {
        "filename": "amazon_prime_titles.csv",
        "label": "Prime",
    },
    "disney": {
        "filename": "disney_plus_titles.csv",
        "label": "Disney+",
    },
}

DATA_DIR = _BACKEND_DIR / "data"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_runtime(row_type: str, duration: str) -> int | None:
    """
    Extract runtime in minutes for Movies; return None for TV Shows.

    Examples:
        "Movie",  "90 min"   → 90
        "TV Show","2 Seasons" → None
    """
    if not isinstance(duration, str) or not duration.strip():
        return None
    if str(row_type).strip().lower() == "movie":
        parts = duration.strip().split()
        if parts and parts[0].isdigit():
            return int(parts[0])
    return None


def ingest(platform_key: str) -> None:
    config = PLATFORM_MAP[platform_key]
    csv_path = DATA_DIR / config["filename"]
    platform_label = config["label"]

    if not csv_path.exists():
        print(f"[ERROR] CSV not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Reading {csv_path} …")
    df = pd.read_csv(csv_path, dtype=str)

    # Normalise column names to lowercase, strip whitespace
    df.columns = [c.strip().lower() for c in df.columns]

    # Required columns present in all three Kaggle CSVs
    required = {"show_id", "type", "title", "release_year"}
    missing = required - set(df.columns)
    if missing:
        print(f"[ERROR] CSV is missing expected columns: {missing}", file=sys.stderr)
        sys.exit(1)

    # Drop rows without a title or release_year
    before = len(df)
    df = df[df["title"].notna() & df["title"].str.strip().ne("")]
    df = df[df["release_year"].notna() & df["release_year"].str.strip().ne("")]
    print(f"[INFO] {before - len(df)} rows skipped (missing title or release_year).")

    create_tables()

    inserted_titles = 0
    inserted_genres = 0
    skipped = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            name = str(row["title"]).strip()
            try:
                release_year = int(float(str(row["release_year"]).strip()))
            except (ValueError, TypeError):
                skipped += 1
                continue

            row_type = str(row.get("type", "")).strip() if pd.notna(row.get("type")) else None
            rating = str(row.get("rating", "")).strip() if pd.notna(row.get("rating")) else None
            rating = rating if rating else None
            country = str(row.get("country", "")).strip() if pd.notna(row.get("country")) else None
            country = country if country else None
            description = str(row.get("description", "")).strip() if pd.notna(row.get("description")) else None
            description = description if description else None
            duration_raw = str(row.get("duration", "")).strip() if pd.notna(row.get("duration")) else None
            runtime_min = _parse_runtime(row_type, duration_raw)

            # INSERT OR IGNORE based on unique constraint (name, release_year, platform)
            result = conn.execute(
                titles.insert().prefix_with("OR IGNORE").values(
                    name=name,
                    type=row_type,
                    release_year=release_year,
                    rating=rating,
                    vote_count=None,
                    runtime_min=runtime_min,
                    language=None,
                    country=country,
                    platform=platform_label,
                    description=description,
                )
            )

            if result.rowcount == 1:
                inserted_titles += 1
                title_id = result.lastrowid
            else:
                # Row already existed — look up its id for genre linking
                skipped += 1
                existing = conn.execute(
                    select(titles.c.id).where(
                        (titles.c.name == name)
                        & (titles.c.release_year == release_year)
                        & (titles.c.platform == platform_label)
                    )
                ).fetchone()
                if existing is None:
                    continue
                title_id = existing[0]

            # Insert genres (INSERT OR IGNORE for idempotency)
            listed_in = row.get("listed_in", "")
            if pd.notna(listed_in) and str(listed_in).strip():
                for genre in str(listed_in).split(","):
                    genre = genre.strip()
                    if not genre:
                        continue
                    g_result = conn.execute(
                        title_genres.insert().prefix_with("OR IGNORE").values(
                            title_id=title_id,
                            genre=genre,
                        )
                    )
                    if g_result.rowcount == 1:
                        inserted_genres += 1

    print(f"[DONE] platform={platform_label}")
    print(f"       titles inserted : {inserted_titles}")
    print(f"       titles skipped  : {skipped}")
    print(f"       genres inserted : {inserted_genres}")

    # Quick verification query
    with engine.connect() as conn:
        total_titles = conn.execute(
            text("SELECT COUNT(*) FROM titles WHERE platform = :p"),
            {"p": platform_label},
        ).scalar()
        total_genres = conn.execute(
            text(
                "SELECT COUNT(*) FROM title_genres tg "
                "JOIN titles t ON t.id = tg.title_id "
                "WHERE t.platform = :p"
            ),
            {"p": platform_label},
        ).scalar()
    print(f"[DB]   titles in DB for {platform_label}: {total_titles}")
    print(f"[DB]   genre rows in DB for {platform_label}: {total_genres}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest OTT CSV into SQLite.")
    parser.add_argument(
        "--platform",
        choices=list(PLATFORM_MAP.keys()),
        required=True,
        help="Platform CSV to ingest: netflix | prime | disney",
    )
    args = parser.parse_args()
    ingest(args.platform)


if __name__ == "__main__":
    main()
