from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from . import GenreRelation, GenreRelationIn, GenreRelationUpdate


async def save_to_db(
        db: AsyncSession,
        genre_relation_db: GenreRelation,
        /
) -> GenreRelation:
    try:
        await db.commit()
        await db.refresh(genre_relation_db)
        return genre_relation_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'genre_relations_from_genre_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='from genre not found'
            )
        elif 'genre_relations_to_genre_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='to genre not found'
            )
        elif 'genre_relations_from_genre_id_to_genre_id_key' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Relation already exists'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating genre_relation'
        )


async def create_genre_relation(
        db: AsyncSession,
        genre_relation_scheme: GenreRelationIn,
        /
) -> GenreRelation:
    genre_relation_db = GenreRelation(
        from_genre_id=genre_relation_scheme.from_genre_id,
        to_genre_id=genre_relation_scheme.to_genre_id
    )
    db.add(genre_relation_db)
    genre_relation_db = await save_to_db(db, genre_relation_db)
    return genre_relation_db


async def update_genre_relation(
        db: AsyncSession,
        genre_relatin_scheme: GenreRelationUpdate,
        genre_relation_id: UUID,
        exclude_unset: bool = False,
        /
) -> GenreRelation:
    genre_relation_db = await verify_genre_relation(db, genre_relation_id)
    for field, value in genre_relatin_scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(genre_relation_db, field, value)
    genre_relation_db = await save_to_db(db, genre_relation_db)
    return genre_relation_db


async def verify_genre_relation(
        db: AsyncSession,
        genre_relation_id: UUID,
        /
) -> GenreRelation:
    genre_relation_db = await db.get(GenreRelation, genre_relation_id)
    if not genre_relation_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Genre relation not found'
        )
    return genre_relation_db


async def delete_genre_relation(
        db: AsyncSession,
        genre_relation_id: UUID,
        /
) -> None:
    genre_relation_db = await verify_genre_relation(db, genre_relation_id)
    await db.delete(genre_relation_db)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error deleting genre relation'
        )