from abc import ABC, abstractmethod
from typing import Tuple

from app import schemas


class ErrorFetchFailed(Exception):
    pass


class MusicService(ABC):
    """
    Defines the interface of the connectors
    """

    @classmethod
    @abstractmethod
    async def create(cls, *args, **kwargs):
        """
        Instantiate the service connector and returns its own class
        """
        pass

    @abstractmethod
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
        pass
