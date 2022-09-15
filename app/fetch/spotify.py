import asyncio
import base64
from typing import Tuple

import httpx
from fastapi.encoders import jsonable_encoder

from app import schemas
from app.fetch.service import ErrorFetchFailed, MusicService
from app.logger import log_call, logger


class Spotify(MusicService):
    """
    The connector to Spotify
    """

    TOKEN_URI = "https://accounts.spotify.com/api/token"

    @classmethod
    async def create(cls, client_id: str, client_secret: str):
        connector = cls()
        connector.client_id = client_id
        connector.client_secret = client_secret
        connector.auth_token = await connector._get_token()
        return connector

    async def _get_token(self) -> Tuple[str, int]:
        message = f"{self.client_id}:{self.client_secret}"
        base64Message = base64.b64encode(message.encode("ascii")).decode("ascii")

        headers = {"Authorization": f"Basic {base64Message}"}
        data = {"grant_type": "client_credentials"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.TOKEN_URI, headers=headers, data=data)
        resp_as_dict = resp.json()
        auth_token = resp_as_dict["access_token"]
        return auth_token

    @log_call
    async def fetch(self, artist_id: str) -> Tuple[str, schemas.ArtistUpdate]:
        """
        Fetch one artist from Spotify
        Return:
            artist_id, schemas.ArtistUpdate
        """
        # async with httpx.AsyncClient() as client:
        #     # TODO make it real
        #     resp = await client.post()
        # if resp.status_code >= 300:  # it's an error
        #     fail_message = (
        #         f"HTTP {resp.status_code}: Failed to fetch artist {artist_id}"
        #     )
        #     # logger.error("%s", failed_message)
        #     raise ErrorFetchFailed(fail_message)

        # TODO dummy fixed ret value to try things out
        return (
            "4awnjjqiUnSBA4ucPVbF8R",
            schemas.ArtistUpdate(name="Sto Cavolo", popularity=9),
        )


spotify = Spotify()
