from abc import ABC, abstractmethod
from typing import Iterable

from app import schemas


class ErrorFetchFailed(Exception):
    pass


class FetchConnectorService(ABC):
    """
    Defines the functionality offered by the connectors
    """

    @abstractmethod
    @classmethod
    async def create(cls, *args, **kwargs):
        pass

    @abstractmethod
    async def fetch(self, artist_id: str) -> schemas.ArtistUpdate:
        """
        Fetch one artist from the music archive provider
        Params:
            artist_id: the artist id
        Raise
            ErrorFetchFailed when it fails
        """
        pass
