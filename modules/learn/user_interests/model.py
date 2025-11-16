from datetime import datetime, timezone
from enum import IntEnum as py_enum
from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import uuid4, UUID
from database import Base


class InterestDegree(py_enum):

    level_1 = 1
    level_2 = 2
    level_3 = 3
    level_4 = 4
    level_5 = 5


class UserInterest(Base):
    __tablename__ = 'user_interests'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    degree: Mapped[InterestDegree] = mapped_column(Integer, nullable=False)
    book_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    book: Mapped['Book'] = relationship(
        'Book',
        foreign_keys=[book_id],
        back_populates='user_interest',
        lazy='selectin'
    )

    user: Mapped['User'] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='user_interest',
        lazy='noload'
    )