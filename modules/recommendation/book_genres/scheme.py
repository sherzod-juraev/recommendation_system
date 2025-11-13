from pydantic import BaseModel
from uuid import UUID
from ..genres import GenreOut


class BookInfo(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    title: str


class BookGenreOut(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    book: BookInfo
    genre: GenreOut


class BookGenreIn(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    book_id: UUID
    genre_id: UUID


class BookGenreUpdate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    book_id: UUID | None = None
    genre_id: UUID | None = None