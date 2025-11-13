from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import uuid4, UUID
from database import Base


class GenreRelation(Base):
    __tablename__ = 'genre_relations'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    from_genre_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('genres.id', ondelete='CASCADE'), nullable=False)
    to_genre_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('genres.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    from_genre: Mapped['Genre'] = relationship(
        'Genre',
        foreign_keys=[from_genre_id],
        back_populates='genre_head',
        lazy='selectin'
    )

    to_genre: Mapped['Genre'] = relationship(
        'Genre',
        foreign_keys=[to_genre_id],
        back_populates='genre_last',
        lazy='selectin'
    )

    __table_args__ = (
        UniqueConstraint('from_genre_id', 'to_genre_id'),
    )