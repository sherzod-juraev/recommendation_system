from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct
from uuid import UUID
from ...learn.related_genres import GenreRelation


async def get_interest(
        db: AsyncSession,
        genres_id_set: set,
        /
) -> set[UUID]:
    query = select(distinct(GenreRelation.to_genre_id)).where(
        GenreRelation.from_genre_id.in_(genres_id_set),
        GenreRelation.to_genre_id.notin_(genres_id_set)
    ).limit(100)
    result = await db.execute(query)
    genres_id = set(result.scalars().all())
    return genres_id