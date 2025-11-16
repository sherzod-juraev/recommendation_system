from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct
from uuid import UUID
from ...recommendation.book_genres import BookGenre
from ...learn.user_interests import UserInterest
from .select_from_db import get_interest


async def conclusion(
        db: AsyncSession,
        user_id: UUID,
        genres_id_set: set,
        /
) -> set[UUID]:
    genres_id = await get_interest(db, genres_id_set)
    # yangi janrdagi kitoblar
    query = select(distinct(BookGenre.book_id)).where(
        BookGenre.genre_id.in_(genres_id)
    ).limit(100)
    result = await db.execute(query)
    books_id_set = set(result.scalars().all())
    # user o'qiganlari
    query = select(distinct(UserInterest)).where(
        UserInterest.book_id.in_(books_id_set)
    )
    result = await db.execute(query)
    books_read = set(result.scalars().all())
    books_id_set -= books_read
    return books_id_set