from abc import ABC, abstractmethod
from typing import Iterable

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
    async def fetch(self, artist_id: str) -> schemas.ArtistUpdate:
        """
        Fetch one artist from the music archive provider
        Params:
            artist_id: the artist id
        Raise:
            ErrorFetchFailed when it fails
        """
        pass
