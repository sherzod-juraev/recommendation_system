from pydantic import BaseModel, model_validator
from fastapi import HTTPException, status
from uuid import UUID
from ...recommendation.genres import GenreOut


class GenreRelationOut(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    from_genre: GenreOut
    to_genre: GenreOut


class GenreRelationIn(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    from_genre_id: UUID
    to_genre_id: UUID


    @model_validator(mode='after')
    def verify_object(self) -> 'GenreRelationIn':
        if self.from_genre_id == self.to_genre_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Genres are wrong'
            )
        return self


class GenreRelationUpdate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    from_genre_id: UUID | None = None
    to_genre_id: UUID | None = None


    @model_validator(mode='after')
    def verify_object(self) -> 'GenreRelationUpdate':
        if self.from_genre_id == self.to_genre_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Genres are wrong'
            )
        return self