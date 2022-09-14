from typing import Any

from pydantic import BaseModel

from .artist import Artist, ArtistCreate, ArtistUpdate
from .typing import CreateType, ModelType, UpdateType


class Message(BaseModel):
    detail: str


class ErrorModel(BaseModel):
    class_name: str
    value: Any


__all__ = [
    "Message",
    "Artist",
    "ArtistCreate",
    "ArtistUpdate",
    "CreateType",
    "ModelType",
    "UpdateType",
]
