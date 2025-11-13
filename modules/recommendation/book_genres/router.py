from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database import get_db
from . import BookGenre, BookGenreIn, BookGenreUpdate, BookGenreOut, crud


book_genre_router = APIRouter()


@book_genre_router.post(
    '/',
    summary='Create book_genre',
    status_code=status.HTTP_201_CREATED,
    response_model=BookGenreOut
)
async def create_book_genre(
        book_genre_scheme: BookGenreIn,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> BookGenre:
    book_genre_db = await crud.create_book_genre(db, book_genre_scheme)
    return book_genre_db


@book_genre_router.put(
    '/{book_genre_id}',
    summary='Book genre full update',
    status_code=status.HTTP_200_OK,
    response_model=BookGenreOut
)
async def full_update(
        book_genre_id: UUID,
        book_genre_scheme: BookGenreUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> BookGenre:
    book_genre_db = await crud.update_book_genre(db, book_genre_scheme, book_genre_id)
    return book_genre_db


@book_genre_router.patch(
    '/{book_genre_id}',
    summary='Book genre partial update',
    status_code=status.HTTP_200_OK,
    response_model=BookGenreOut
)
async def partial_update(
        book_genre_id: UUID,
        book_genre_scheme: BookGenreUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> BookGenre:
    book_genre_db = await crud.update_book_genre(db, book_genre_scheme, book_genre_id, True)
    return book_genre_db


@book_genre_router.delete(
    '/{book_genre_id}',
    summary='Delete book genre',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_book_genre(
        book_genre_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_book_genre(db, book_genre_id)


@book_genre_router.get(
    '/{book_genre_id}',
    summary='Get book genre by id',
    status_code=status.HTTP_200_OK,
    response_model=BookGenreOut
)
async def get_book_genre(
        book_genre_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> BookGenre:
    book_genre_db = await crud.verify_book_genre(db, book_genre_id)
    return book_genre_db