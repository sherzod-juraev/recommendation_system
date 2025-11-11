from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from .model import Sender


class ContentOut(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    sender: Sender
    text: str
    data: list[float]
    created_at: datetime


class ContentIn(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    text: str
    sender: Sender = Sender.user
    data: list[float]
    chat_id: UUID