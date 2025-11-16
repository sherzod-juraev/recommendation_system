from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct
from uuid import UUID
from ...learn.user_interests import UserInterest
from ...recommendation.books import Book


async def get_interest(
        db: AsyncSession,
        user_id: UUID,
        /
) -> set[UUID]:
    query = select(distinct(Book.author_id)).join(
        Book.user_interest
    ).where(
        UserInterest.user_id == user_id
    ).where(
        UserInterest.degree >= 3
    ).limit(5)
    result = await db.execute(query)
    authors_set = set(result.scalars().all())

    return authors_set