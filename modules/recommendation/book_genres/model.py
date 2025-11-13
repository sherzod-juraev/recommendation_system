from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import uuid4, UUID
from database import Base


class BookGenre(Base):
    __tablename__ = 'book_genre'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    book_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    genre_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('genres.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    book: Mapped['Book'] = relationship(
        'Book',
        foreign_keys=[book_id],
        back_populates='book_genres',
        lazy='selectin'
    )

    genre: Mapped['Genre'] = relationship(
        'Genre',
        foreign_keys=[genre_id],
        back_populates='book_genre',
        lazy='selectin'
    )