from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from core import settings


sqlalchemy_async_engine = create_async_engine(
    url=settings.database_url,
    pool_size=30,
    max_overflow=60,
    pool_recycle=1800,
    pool_timeout=10
)

sqlalchemy_async_session = async_sessionmaker(bind=sqlalchemy_async_engine)
Base = declarative_base()