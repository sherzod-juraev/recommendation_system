from pydantic import BaseModel
from uuid import UUID


class BookOut(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    title: str


class BookIn(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    title: str
    author_id: UUID


class BookUpdate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    title: str | None = None
    author_id: UUID | None = None