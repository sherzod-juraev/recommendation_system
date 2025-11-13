from pydantic import BaseModel
from uuid import UUID
from ..genres import GenreOut


class BookGenre(BaseModel):
    model_config = {
        'from_attributes': True
    }

    genre: GenreOut


class BookOut(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    title: str
    book_genres: list[BookGenre] = []


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