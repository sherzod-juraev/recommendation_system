from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct
from uuid import UUID
from ...recommendation.books import Book
from ...learn.user_interests import UserInterest
from .select_from_db import get_interest


async def conclusion(
        db: AsyncSession,
        user_id: UUID,
        /
) -> set[UUID]:
    # qiziqqan mualliflari
    authors_id_set = await get_interest(db, user_id)
    # shu mualliflarning kitoblari
    query = select(Book.id).where(
        Book.author_id.in_(authors_id_set)
    ).order_by(Book.created_at.desc()).limit(100)
    result = await db.execute(query)
    books_id_set = set(result.scalars().all())
    # user o'qigan kitoblar
    query = select(distinct(
        UserInterest.book_id)).where(
        UserInterest.book_id.in_(books_id_set))
    result = await db.execute(query)
    books_read = set(result.scalars().all())
    # tavsiya etiladigan kitoblar
    books_id_set -= books_read
    return books_id_set