from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class ChatOut(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    title: str
    created_at:datetime


class ChatIn(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    title: str