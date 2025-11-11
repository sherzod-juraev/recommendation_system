from .connection import sqlalchemy_async_session
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:

    async with sqlalchemy_async_session() as session:
        try:
            yield session
        except Exception as exc:
            await session.rollback()
            raise exc
        finally:
            await session.close()