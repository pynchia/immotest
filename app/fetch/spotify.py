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
    GET_ARTIST_URI = "https://api.spotify.com/v1/artists/{id}"

    @classmethod
    async def create(cls, client_id: str, client_secret: str):
        connector = cls()
        connector.client_id = client_id
        connector.client_secret = client_secret
        connector.auth_token_header = await connector._get_token_header()
        return connector

    @log_call
    async def _get_token_header(self) -> Tuple[str, int]:
        """
        Retrieve the auth token
        Params:
            client_id
            client_secret
        Return:
            the auth token header to be used in requests

        Note: it is quite simple, given this is a test assignment.
        In reality it would check for errors and most of all
        it would make use of the refresh token
        """
        message = f"{self.client_id}:{self.client_secret}"
        base64Message = base64.b64encode(message.encode("ascii")).decode("ascii")

        headers = {"Authorization": f"Basic {base64Message}"}
        data = {"grant_type": "client_credentials"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.TOKEN_URI, headers=headers, data=data)
        resp_as_dict = resp.json()
        auth_token = resp_as_dict["access_token"]
        logger.debug("Spotify token=%s", auth_token)
        return {"Authorization": f"Bearer {auth_token}"}

    @log_call
    async def fetch(self, artist_id: str) -> Tuple[str, schemas.ArtistUpdate]:
        """
        Fetch one artist from the music archive provider
        Params:
            artist_id: the artist id
        Return:
            the id of the artist
            the artist as an update schema
        Raise:
            ErrorFetchFailed when it fails
        """
        async with httpx.AsyncClient() as client:
            # TODO make it real
            resp = await client.get(
                self.GET_ARTIST_URI.format(id=artist_id), headers=self.auth_token_header
            )
        if resp.status_code >= 300:  # it's an error
            fail_message = (
                f"HTTP {resp.status_code}: Failed to fetch artist {artist_id}"
            )
            logger.error("%s", fail_message)
            raise ErrorFetchFailed(fail_message)
        artist = resp.json()
        return (
            artist["id"],
            schemas.ArtistUpdate(name=artist["name"], popularity=artist["popularity"]),
        )


spotify = Spotify()
