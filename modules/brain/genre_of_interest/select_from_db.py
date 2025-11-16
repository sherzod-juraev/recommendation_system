from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...learn.user_interests import UserInterest
from uuid import UUID


async def get_interest(
        db: AsyncSession,
        user_id: UUID,
        /
) -> list[str]:
    query = select(UserInterest).where(UserInterest.user_id == user_id).order_by(UserInterest.created_at.desc()).limit(20)
    result = await db.execute(query)
    user_interests = result.scalars().all()
    length = len(user_interests)
    genres_id_set = set({})
    books_id_set = set({})
    for i in range(length):
        genre_length = len(user_interests[i].book.book_genres)
        for j in range(genre_length):
            genres_id_set.add(user_interests[i].book.book_genres[j].genre.id)
            books_id_set.add(user_interests[i].book_id)
    array = [list(genres_id_set), list(books_id_set)]
    return array