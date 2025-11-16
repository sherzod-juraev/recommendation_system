from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from ..genre_of_interest import conclusion as genre_conclusion
from ..genre_of_interest.select_from_db import get_interest as genre_interest
from ..interested_authors import conclusion as authors_conclusion
from ..interested_in_related_genres import conclusion as related_genres_conclusion
from ...recommendation.books import Book


async def hybrid_conclusion(
        db: AsyncSession,
        user_id: UUID,
        /
) -> list[Book]:
    books_id_from_genres = await genre_conclusion(db, user_id)
    book_id_from_authors = await authors_conclusion(db, user_id)
    genres_id_set = await genre_interest(db, user_id)
    books_id_from_related_genres = await related_genres_conclusion(db, user_id, genres_id_set)
    books_id_set = books_id_from_genres | book_id_from_authors
    books_id_set = books_id_set | books_id_from_related_genres
    query = select(Book).where(
        Book.id.in_(books_id_set)
    )
    result = await db.execute(query)
    books_list = result.scalars().all()
    return books_list