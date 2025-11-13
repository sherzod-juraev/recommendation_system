from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from . import Genre, GenreIn


async def save_to_db(
        db: AsyncSession,
        genre_db: Genre,
        /
) -> Genre:
    try:
        await db.commit()
        await db.refresh(genre_db)
        return genre_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'genres_name_key' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Name already exists'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating genre'
        )


async def create_genre(
        db: AsyncSession,
        genre_scheme: GenreIn,
        /
) -> Genre:
    genre_db = Genre(name=genre_scheme.name)
    db.add(genre_db)
    genre_db = await save_to_db(db, genre_db)
    return genre_db


async def update_genre(
        db: AsyncSession,
        genre_scheme: GenreIn,
        genre_id: UUID,
        exclude_unset: bool = False,
        /
) -> Genre:
    genre_db = await verify_genre(db, genre_id)
    for field, value in genre_scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(genre_db, field, value)
    genre_db = await save_to_db(db, genre_db)
    return genre_db


async def delete_genre(
        db: AsyncSession,
        genre_id: UUID,
        /
) -> None:
    genre_db = await verify_genre(db, genre_id)
    await db.delete(genre_db)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error deleting genre'
        )


async def verify_genre(
        db: AsyncSession,
        genre_id: UUID,
        /
) -> Genre:
    genre_db = await db.get(Genre, genre_id)
    if not genre_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Genre not found'
        )
    return genre_db