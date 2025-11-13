from datetime import datetime, timezone
from sqlalchemy import Text, DateTime
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import uuid4, UUID
from database import Base


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    book_genre: Mapped['BookGenre'] = relationship(
        'BookGenre',
        foreign_keys='BookGenre.genre_id',
        back_populates='genre',
        passive_deletes=True,
        lazy='noload'
    )