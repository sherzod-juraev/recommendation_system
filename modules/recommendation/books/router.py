from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database import get_db
from . import Book, BookIn, BookUpdate, BookOut, crud


book_router = APIRouter()


@book_router.post(
    '/',
    summary='Create book',
    status_code=status.HTTP_201_CREATED,
    response_model=BookOut
)
async def create_book(
        book_scheme: BookIn,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Book:
    book_db = await crud.create_book(db, book_scheme)
    return book_db


@book_router.put(
    '/{book_id}',
    summary='Book full update',
    status_code=status.HTTP_200_OK,
    response_model=BookOut
)
async def full_update(
        book_id: UUID,
        book_scheme: BookUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Book:
    book_db = await crud.update_book(db, book_scheme, book_id)
    return book_db


@book_router.patch(
    '/{book_id}',
    summary='Book partial update',
    status_code=status.HTTP_200_OK,
    response_model=BookOut
)
async def partial_update(
        book_id: UUID,
        book_scheme: BookUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Book:
    book_db = await crud.update_book(db, book_scheme, book_id, True)
    return book_db


@book_router.delete(
    '/{book_id}',
    summary='Delete book',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_book(
        book_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_book(db, book_id)


@book_router.get(
    '/{book_id}',
    summary='Get book by id',
    status_code=status.HTTP_200_OK,
    response_model=BookOut
)
async def get_book(
        book_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Book:
    book_db = await crud.verify_book(db, book_id)
    return book_db