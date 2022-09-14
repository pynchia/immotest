import asyncio
import base64
from typing import Tuple

import httpx
from fastapi.encoders import jsonable_encoder

from app import schemas
from app.core.config import settings
from app.fetch.service import ErrorFetchFailed, FetchConnectorService


class Spotify(FetchConnectorService):
    """
    The connector to Spotify
    """

    TOKEN_URI = "https://accounts.spotify.com/api/token"

    @classmethod
    async def create(cls, client_id: str, client_secret: str):
        connector = cls()
        connector.client_id = client_id
        connector.client_secret = client_secret
        connector.auth_token = await connector.get_token()

    async def get_token(self) -> Tuple[str, int]:
        message = f"{self.client_id}:{self.client_secret}"
        base64Message = base64.b64encode(message.encode("ascii")).decode("ascii")

        headers = {"Authorization": f"Basic {base64Message}"}
        data = {"grant_type": "client_credentials"}
        resp = httpx.post(self.TOKEN_URI, headers=headers, data=data)
        resp_as_dict = resp.json()
        auth_token = resp_as_dict["access_token"]
        return auth_token

    async def fetch(self, artist_id: str) -> schemas.ArtistUpdate:
        async with httpx.AsyncClient() as client:
            resp = await client.post()
        if resp.status_code >= 300:  # it's an error
            fail_message = (
                f"HTTP {resp.status_code}: Failed to fetch artist {artist_id}"
            )
            # logger.error("%s", failed_message)
            raise ErrorFetchFailed(fail_message)


spotify = Spotify()
