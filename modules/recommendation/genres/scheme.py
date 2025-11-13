from pydantic import BaseModel
from uuid import UUID


class GenreOut(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    name: str


class GenreIn(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    name: str