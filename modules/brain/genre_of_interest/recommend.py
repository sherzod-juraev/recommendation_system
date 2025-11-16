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
) -> set[UUID]:
    genres_id_list = await get_interest(db, user_id)
    # janrlarda yozilgan kitoblar
    query = select(distinct(UserInterest.book_id)).join(
        UserInterest.book
    ).join(
        Book.book_genres
    ).where(
        BookGenre.genre_id.in_(genres_id_list)
    ).limit(100)
    result = await db.execute(query)
    books_id_list = set(result.scalars().all())
    # o'qilgan kitoblar
    query = select(distinct(UserInterest.book_id)).where(
        UserInterest.user_id == user_id
    )
    result = await db.execute(query)
    books_read = set(result.scalars().all())
    books_id_list -= books_read
    return books_id_list