from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from . import BookGenre, BookGenreIn, BookGenreUpdate


async def save_to_db(
        db: AsyncSession,
        book_genre_db: BookGenre,
        /
) -> BookGenre:
    try:
        await db.commit()
        await db.refresh(book_genre_db)
        return book_genre_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'book_genre_book_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Book not found'
            )
        elif 'book_genre_genre_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Genre not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating book_genre'
        )


async def create_book_genre(
        db: AsyncSession,
        book_genre_scheme: BookGenreIn,
        /
) -> BookGenre:
    book_genre_db = BookGenre(
        book_id=book_genre_scheme.book_id,
        genre_id=book_genre_scheme.genre_id
    )
    db.add(book_genre_db)
    book_genre_db = await save_to_db(db, book_genre_db)
    return book_genre_db


async def update_book_genre(
        db: AsyncSession,
        book_genre_scheme: BookGenreUpdate,
        book_genre_id: UUID,
        exclude_unset: bool = False,
        /
) -> BookGenre:
    book_genre_db = await verify_book_genre(db, book_genre_id)
    for field, value in book_genre_scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(book_genre_db, field, value)
    book_genre_db = await save_to_db(db, book_genre_db)
    return book_genre_db


async def delete_book_genre(
        db: AsyncSession,
        book_genre_id: UUID,
        /
) -> None:
    book_genre_db = await verify_book_genre(db, book_genre_id)
    await db.delete(book_genre_db)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error deleting book_genre'
        )


async def verify_book_genre(
        db: AsyncSession,
        book_genre_id: UUID,
        /
) -> BookGenre:
    book_genre_db = await db.get(BookGenre, book_genre_id)
    if not book_genre_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book_genre not found'
        )
    return book_genre_db