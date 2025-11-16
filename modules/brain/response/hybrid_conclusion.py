from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from sqlalchemy.util import await_only

from ..genre_of_interest import conclusion as genre_conclusion
from ...recommendation.books import Book


async def hybrid_conclusion(
        db: AsyncSession,
        user_id: UUID,
        /
) -> list[Book]:
    # faqatgina genre bo'yicha natija chiqaramiz
    return await genre_conclusion(db, user_id)