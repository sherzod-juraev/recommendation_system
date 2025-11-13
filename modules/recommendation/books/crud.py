from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from . import Book, BookIn, BookUpdate


async def save_to_db(
        db: AsyncSession,
        book_db: Book,
        /
) -> Book:
    try:
        await db.commit()
        await db.refresh(book_db)
        return book_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'books_author_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Author not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating books'
        )


async def create_book(
        db: AsyncSession,
        book_scheme: BookIn,
        /
) -> Book:
    book_db = Book(
        title=book_scheme.title,
        author_id=book_scheme.author_id
    )
    db.add(book_db)
    book_db = await save_to_db(db, book_db)
    return book_db


async def update_book(
        db: AsyncSession,
        book_scheme: BookUpdate,
        book_id: UUID,
        exclude_unset: bool = False,
        /
) -> Book:
    book_db = await verify_book(db, book_id)
    for field, value in book_scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(book_db, field, value)
    book_db = await save_to_db(db, book_db)
    return book_db


async def delete_book(
        db: AsyncSession,
        book_id: UUID,
        /
) -> None:
    book_db = await verify_book(db, book_id)
    await db.delete(book_db)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error deleting book'
        )


async def verify_book(
        db: AsyncSession,
        book_id: UUID,
        /
) -> Book:
    book_db = await db.get(Book, book_id)
    if not book_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return book_db