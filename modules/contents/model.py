from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Text, DateTime, ForeignKey, Enum as db_enum
from sqlalchemy.dialects.postgresql import UUID as db_uuid, JSON
from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import uuid4, UUID
from database import Base


class Sender(Enum):
    user = 'user'
    server = 'server'


class Content(Base):
    __tablename__ = 'contents'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    sender: Mapped[Sender] = mapped_column(db_enum(Sender), nullable=False, default=Sender.server)
    text: Mapped[str | None] = mapped_column(Text)
    data: Mapped[list[float]] = mapped_column(JSON, nullable=False)
    chat_id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    chat: Mapped['Chat'] = relationship(
        'Chat',
        foreign_keys=[chat_id],
        back_populates='contents',
        lazy='noload'
    )
