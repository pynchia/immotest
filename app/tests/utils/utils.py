import random
import string
from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=16))


async def create_artist(
    db_session: AsyncSession,
) -> Tuple[schemas.ArtistCreate, models.Artist]:
    """
    utility function to create an artist
    """
    id_ = random_lower_string()
    name = random_lower_string()
    popularity = 12
    artist_in = schemas.ArtistCreate(id=id_, name=name, popularity=popularity)
    artist = await crud.artist.create(db_session, artist_in)
    assert artist.id == artist_in.id
    assert artist.name == artist_in.name
    assert artist.popularity == artist_in.popularity
    return artist_in, artist
