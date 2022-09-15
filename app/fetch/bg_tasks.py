import asyncio

from sqlalchemy.exc import SQLAlchemyError

from app import crud, models
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
            artists = await crud.artist.list(
                db,
                clauses=[
                    (models.Artist.updated_by_be == False),
                ],
            )
            # fetch_requests = (self.music_connector.fetch(a.id) for a in artists)
            # id_and_artists = await asyncio.gather(
            #     *fetch_requests, return_exceptions=True
            # )
            # Note: we need to issue requests more slowly to Spotify
            # otherwise it complains with a 429
            id_and_artists = []
            for a in artists:  # this loop can be made async
                id_and_artists.append(await self.music_connector.fetch(a.id))
                await asyncio.sleep(1.0)

            # update_ops = (
            #     crud.artist.update(db, obj_in=a, obj_id=id_)
            #     for id_, a in id_and_artists
            # )
            # await asyncio.gather(
            #     *update_ops, return_exceptions=False
            # )  # update artists in db
            # Note: unfortunately the gather does not work, no concurrent db.add
            # before a flush

            for id_, a in id_and_artists:  # this loop can be made async
                await crud.artist.update(db, obj_in=a, obj_id=id_)

    @log_call
    async def run(self):
        """
        Periodically fetch the artists
        """
        while True:
            await self._fetch_artists()
            await asyncio.sleep(self.delay)
