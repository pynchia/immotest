from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import parse_obj_as
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud import artist
from app.exceptions import ModelNotFoundException
from app.schemas import Artist, ArtistCreate, ArtistUpdate, Message

router = APIRouter()


@router.get("/", response_model=List[Artist])
async def read_artists(
    db: AsyncSession = Depends(get_db),
    offset: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> List[Artist]:
    """
    Retrieve all artists
    """

    found_artists = await artist.list(db, offset=offset, limit=limit)
    return parse_obj_as(List[Artist], found_artists)


@router.get("/{id}", response_model=Artist, responses={404: {"model": Message}})
async def read_artist(*, db: AsyncSession = Depends(get_db), id: str) -> Artist:
    """
    Get artist by ID
    """

    try:
        found_artist = await artist.get(db, id)
        return parse_obj_as(Artist, found_artist)
    except ModelNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found"
        ) from error


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Artist,
    responses={409: {"model": Message}},
)
async def create_artist(
    *, db: AsyncSession = Depends(get_db), item_in: ArtistCreate
) -> Artist:
    """
    Create an artist
    """

    try:
        created_artist = await artist.create(db, item_in)
        return parse_obj_as(Artist, created_artist)
    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Artist already exist"
        )


@router.put(
    "/{id}",
    response_model=Artist,
    responses={404: {"model": Message}, 400: {"model": Message}},
)
async def update_artist(
    *, db: AsyncSession = Depends(get_db), id: str, item_in: ArtistUpdate
) -> Artist:
    """
    Update an artist
    """

    try:
        updated_artist = await artist.update(db, item_in, id)
        return parse_obj_as(Artist, updated_artist)
    except ModelNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found"
        ) from error


@router.delete("/{id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
async def delete_artist(*, db: AsyncSession = Depends(get_db), id: str) -> None:
    """
    Delete an artist
    """

    try:
        await artist.delete(db, id)
    except ModelNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found",
        ) from error
