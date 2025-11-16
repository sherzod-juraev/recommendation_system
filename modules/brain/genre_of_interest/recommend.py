from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct
from uuid import UUID
from .select_from_db import get_interest
from ...learn.user_interests import UserInterest
from ...recommendation.books import Book
from ...recommendation.book_genres import BookGenre


async def conclusion(
        db: AsyncSession,
        user_id: UUID,
        /
) -> list[Book]:
    result = await get_interest(db, user_id)
    genres_id_list, books_id_list = result[0], result[1]
    query = select(distinct(UserInterest.book_id)).join(
        UserInterest.book
    ).join(
        Book.book_genres
    ).where(
        UserInterest.book_id.notin_(books_id_list),
        BookGenre.genre_id.in_(genres_id_list)
    )
    result = await db.execute(query)
    books_id_list = result.scalars().all()
    query = select(Book).where(Book.id.in_(books_id_list)).order_by(Book.title.asc())
    result = await db.execute(query)
    books_list = result.scalars().all()
    return books_list