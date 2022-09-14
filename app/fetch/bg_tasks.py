import asyncio

from sqlalchemy.exc import SQLAlchemyError

from app import crud
from app.core.config import settings
from app.db import async_session
from app.fetch.service import ErrorFetchFailed, MusicService
from app.logger import log_call, logger


class ArtistFetcher:
    """
    Periodically fetch artists from the music archive provider
    """

    def __init__(self, *, music_connector: MusicService, delay: float):
        """
        Params:
            delay: the number of seconds to sleep before polling the dir again
        """
        self.music_connector = music_connector
        self.delay = delay

    @log_call
    async def _fetch_artists(self) -> None:
        """
        Fetch the artists once
        """
        async with async_session() as db:
            # TODO read suitable artists from the DB
            artists = await crud.artist.list(db)
            fetch_requests = (self.music_connector.fetch(a.id) for a in artists)
            artists = await asyncio.gather(*fetch_requests, return_exceptions=True)
            logger.debug(str(artists))

    @log_call
    async def run(self):
        """
        Periodically fetch the artists
        """
        while True:
            await self._fetch_artists()
            await asyncio.sleep(self.delay)
