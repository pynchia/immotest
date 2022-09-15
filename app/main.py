import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.fetch.bg_tasks import ArtistFetcher
from app.fetch.spotify import Spotify
from app.logger import logger

DB_DELAY = 3.0


app = FastAPI(
    title="immotest",
    description="a test",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.on_event("startup")
async def bg_fetcher():
    spotify_connector = await Spotify.create(
        settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET
    )
    artist_fetcher = ArtistFetcher(
        music_connector=spotify_connector,
        delay=settings.FETCH_ARTIST_DELAY,
    )
    asyncio.create_task(artist_fetcher.run())
