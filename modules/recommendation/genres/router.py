from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database import get_db
from . import Genre, GenreIn, GenreOut, crud


genre_router = APIRouter()


@genre_router.post(
    '/',
    summary='Create genre',
    status_code=status.HTTP_201_CREATED,
    response_model=GenreOut
)
async def create_genre(
        genre_scheme: GenreIn,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Genre:
    genre_db = await crud.create_genre(db, genre_scheme)
    return genre_db


@genre_router.put(
    '/{genre_id}',
    summary='Genre full update',
    status_code=status.HTTP_200_OK,
    response_model=GenreOut
)
async def full_update(
        genre_id: UUID,
        genre_scheme: GenreIn,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Genre:
    genre_db = await crud.update_genre(db, genre_scheme, genre_id)
    return genre_db


@genre_router.delete(
    '/{genre_id}',
    summary='Delete genre',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_genre(
        genre_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_genre(db, genre_id)


@genre_router.get(
    '/{genre_id}',
    summary='Get genre',
    status_code=status.HTTP_200_OK,
    response_model=GenreOut
)
async def get_genre(
        genre_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Genre:
    genre_db = await crud.verify_genre(db, genre_id)
    return genre_db