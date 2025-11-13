from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete
from fastapi import HTTPException, status
from uuid import UUID
from . import Author, AuthorIn


async def save_to_db(
        db: AsyncSession,
        author_db: Author,
        /
) -> Author:
    try:
        await db.commit()
        await db.refresh(author_db)
        return author_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'authors_full_name_key' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Full name already exists'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating author'
        )


async def create_author(
        db: AsyncSession,
        author_scheme: Author,
        /
) -> Author:
    author_db = Author(
        full_name=author_scheme.full_name
    )
    db.add(author_db)
    author_db = await save_to_db(db, author_db)
    return author_db


async def update_author(
        db: AsyncSession,
        author_scheme: AuthorIn,
        author_id: UUID,
        exclude_unset: bool = False,
        /
) -> Author:
    author_db = await verify_author(db, author_id)
    for field, value in author_scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(author_db, field, value)
    author_db = await save_to_db(db, author_db)
    return author_db


async def delete_author(
        db: AsyncSession,
        author_id: UUID,
        /
) -> Author:
    query = delete(Author).where(Author.id == author_id)
    result = await db.execute(query)
    try:
        await db.commit()
        if result.rowcount != 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Author not found'
            )
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error deleting author'
        )


async def verify_author(
        db: AsyncSession,
        author_id: UUID,
        /
) -> Author:
    author_db = await db.get(Author, author_id)
    print(author_db.books)
    if not author_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Author not found'
        )
    return author_db
