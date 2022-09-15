import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.exceptions import ModelNotFoundException
from app.schemas import Artist, ArtistCreate, ArtistUpdate
from app.tests.utils import create_artist, random_lower_string


@pytest.mark.asyncio
async def test_create_artist_success(db_session: AsyncSession) -> None:
    artist_in, artist = await create_artist(db_session)
    assert artist.id == artist_in.id
    assert artist.name == artist_in.name
    assert artist.popularity == artist_in.popularity


@pytest.mark.asyncio
async def test_create_artist_fail_artist_already_exists(
    db_session: AsyncSession,
) -> None:
    _, artist = await create_artist(db_session)
    artist_in_2 = ArtistCreate(
        id=artist.id, name=artist.name + "XYZ", popularity=artist.popularity + 30
    )
    with pytest.raises(IntegrityError):
        await crud.artist.create(db_session, artist_in_2)


@pytest.mark.asyncio
async def test_get_artist_success(db_session: AsyncSession) -> None:
    _, artist = await create_artist(db_session)
    stored_artist = await crud.artist.get(db_session, artist.id)
    assert artist.id == stored_artist.id
    assert artist.name == stored_artist.name
    assert artist.popularity == stored_artist.popularity


@pytest.mark.asyncio
async def test_get_artist_fail_artist_not_found(db_session: AsyncSession) -> None:
    artist_id = random_lower_string()
    with pytest.raises(ModelNotFoundException):
        await crud.artist.get(db_session, artist_id)


@pytest.mark.asyncio
async def test_update_artist_success(db_session: AsyncSession) -> None:
    _, artist = await create_artist(db_session)
    artist_name = artist.name
    new_name = artist_name + "XYZ"
    artist_in_2 = ArtistUpdate(name=new_name)
    updated_artist = await crud.artist.update(
        db_session, artist_in_2, artist.id, updated_by_be=True
    )
    assert updated_artist.id == artist.id
    assert updated_artist.name != artist_name
    assert updated_artist.name == new_name
    assert updated_artist.popularity == artist.popularity
    assert updated_artist.updated_by_be == True


@pytest.mark.asyncio
async def test_delete_artist(db_session: AsyncSession) -> None:
    _, artist = await create_artist(db_session)
    await crud.artist.delete(db_session, artist.id)
    with pytest.raises(ModelNotFoundException):
        artist2 = await crud.artist.get(db_session, artist.id)
        assert artist2 is None


@pytest.mark.parametrize(
    "clauses,expected_num_artists",
    [
        (
            [],
            11,
        ),
        (
            [
                (models.Artist.updated_by_be == False),
            ],
            10,
        ),
    ],
    ids=[
        "all artists, empty filter",
        "artists updated by BE",
    ],
)
@pytest.mark.asyncio
async def test_list_artists(
    db_session: AsyncSession, clauses, expected_num_artists
) -> None:
    artist_in = ArtistCreate(id="XYZ", name="Joe Doe", popularity=0)
    artist = await crud.artist.create(db_session, artist_in)  # add artist
    await crud.artist.update(
        db_session,
        obj_in=ArtistUpdate(name=artist_in.name, popularity=0),
        obj_id=artist.id,
        updated_by_be=True,
    )  # update one field

    artists = await crud.artist.list(
        db_session,
        clauses=clauses,
    )
    assert len(artists) == expected_num_artists


# etc etc....
# I am not going to do all of them
