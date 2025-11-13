from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio  import AsyncSession
from uuid import UUID
from database import get_db
from . import Author, AuthorIn, AuthorOut, crud


author_router = APIRouter()


@author_router.post(
    '/',
    summary='Create author',
    status_code=status.HTTP_201_CREATED,
    response_model=AuthorOut
)
async def create_author(
        author_scheme: AuthorIn,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Author:
    author_db = await crud.create_author(db, author_scheme)
    return author_db


@author_router.put(
    '/{author_id}',
    summary='Author full update',
    status_code=status.HTTP_200_OK,
    response_model=AuthorOut
)
async def full_update(
        author_id: UUID,
        author_scheme: AuthorIn,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Author:
    author_db = await crud.update_author(db, author_scheme, author_id)
    return author_db


@author_router.delete(
    '/{author_id}',
    summary='Delete author',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_author(
        author_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_author(db, author_id)


@author_router.get(
    '/{author_id}',
    summary='Get author by id',
    status_code=status.HTTP_200_OK,
    response_model=AuthorOut
)
async def get_author(
        author_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Author:
    author_db = await crud.verify_author(db, author_id)
    return author_db