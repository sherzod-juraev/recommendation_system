from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import uuid4, UUID
from database import Base


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    books: Mapped[list['Book']] = relationship(
        'Book',
        foreign_keys='Book.author_id',
        back_populates='author',
        uselist=True,
        lazy='selectin',
        order_by='Book.created_at.asc()',
        passive_deletes=True
    )

