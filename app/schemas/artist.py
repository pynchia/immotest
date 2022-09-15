from typing import Optional

from pydantic import BaseModel


class ArtistBase(BaseModel):
    """Shared properties"""

    name: str
    popularity: Optional[int] = 0


class ArtistCreate(ArtistBase):
    """Properties to receive on artist creation"""

    id: str


class ArtistUpdate(ArtistBase):
    """Properties to receive on artist update"""


class ArtistInDBBase(ArtistBase):
    """ " Properties shared by models stored in DB"""

    id: str

    class Config:
        orm_mode = True


class Artist(ArtistInDBBase):
    """Properties to return to client"""

    updated_by_be: bool


class ArtistInDB(ArtistInDBBase):
    """ " Properties properties stored in DB"""
