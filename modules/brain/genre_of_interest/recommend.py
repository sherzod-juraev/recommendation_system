from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct
from uuid import UUID
from .select_from_db import get_interest
from ...learn.user_interests import UserInterest
from ...recommendation.books import Book
from ...recommendation.genres import Genre


async def conclusion(
        db: AsyncSession,
        user_id: UUID,
        /
) -> list[Book]:
    genres_id_list = await get_interest(db, user_id)
    query = select(distinct(UserInterest.book_id)).join(
        UserInterest.book, UserInterest.book_id == Book.id
    ).join(
        Book.book_genres
    ).where(
        UserInterest.user_id != user_id,
        UserInterest.degree >= 3
    ).where(
        Genre.id.in_(genres_id_list)
    ).order_by(UserInterest.created_at.desc()).limit(10)
    result = await db.execute(query)
    books_id_list = result.scalars().all()
    query = select(Book).where(Book.id.in_(books_id_list)).order_by(Book.title.asc())
    result = await db.execute(query)
    books_list = result.scalars().all()
    return books_list