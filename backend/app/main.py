from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_tables
from app.routers import genres, ratings, releases, search, trends


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="OTT Analytics API", lifespan=lifespan)

# ---------------------------------------------------------------------------
# CORS — allow the Vite dev server and any deployed frontend origin
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173", "*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(ratings.router, prefix="/api")
app.include_router(genres.router, prefix="/api")
app.include_router(releases.router, prefix="/api")
app.include_router(trends.router, prefix="/api")
app.include_router(search.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
