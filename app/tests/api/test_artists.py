import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.utils import create_artist, random_lower_string


@pytest.mark.asyncio
async def test_create_artist(async_client: AsyncClient) -> None:
    data = {
        "id": random_lower_string(),
        "name": random_lower_string(),
        "popularity": 21,
    }
    response = await async_client.post(
        "/artists/",
        json=data,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["id"] == data["id"]
    assert content["name"] == data["name"]
    assert content["popularity"] == data["popularity"]


@pytest.mark.asyncio
async def test_read_artist(async_client: AsyncClient, db_session: AsyncSession) -> None:
    artist_in, artist = await create_artist(db_session)
    response = await async_client.get(f"/artists/{artist.id}")
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == artist.id
    assert content["name"] == artist.name
    assert content["popularity"] == artist.popularity


# etc etc....
# I am not going to do all of them
