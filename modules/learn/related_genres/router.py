from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database import get_db
from . import GenreRelation, GenreRelationIn, GenreRelationUpdate, GenreRelationOut, crud


genre_relation_router = APIRouter()


@genre_relation_router.post(
    '/',
    summary='Create genre relation',
    status_code=status.HTTP_201_CREATED,
    response_model=GenreRelationOut
)
async def create_genre_relation(
        genre_relation_scheme: GenreRelationIn,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> GenreRelation:
    genre_relation_db = await crud.create_genre_relation(db, genre_relation_scheme)
    return genre_relation_db


@genre_relation_router.put(
    '/{genre_relation_id}',
    summary='Genre relation full update',
    status_code=status.HTTP_200_OK,
    response_model=GenreRelationOut
)
async def full_update(
        genre_relation_id: UUID,
        genre_relation_scheme: GenreRelationUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> GenreRelation:
    genre_relation_db = await crud.update_genre_relation(db, genre_relation_scheme, genre_relation_id)
    return genre_relation_db


@genre_relation_router.patch(
    '/{genre_relation_id}',
    summary='Genre relation partial update',
    status_code=status.HTTP_200_OK,
    response_model=GenreRelationOut
)
async def partial_update(
        genre_relation_id: UUID,
        genre_relation_scheme: GenreRelationUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> GenreRelation:
    genre_relation_db = await crud.update_genre_relation(db, genre_relation_scheme, genre_relation_id, True)
    return genre_relation_db


@genre_relation_router.delete(
    '/{genre_relation_id}',
    summary='Delete genre relation',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_genre_relation(
        genre_relation_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_genre_relation(db, genre_relation_id)


@genre_relation_router.get(
    '/{genre_relation_id}',
    summary='Get genre relation by id',
    status_code=status.HTTP_200_OK,
    response_model=GenreRelationOut
)
async def get_genre_relation(
        genre_relation_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> GenreRelation:
    genre_relation_db = await crud.verify_genre_relation(db, genre_relation_id)
    return genre_relation_db