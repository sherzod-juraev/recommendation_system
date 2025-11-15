from pydantic import BaseModel, model_validator
from fastapi import HTTPException, status
from uuid import UUID
from .model import InterestDegree
from ...recommendation.books import BookOut


class  UserInterestOut(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    degree: InterestDegree
    book: BookOut


class UserInterestIn(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    degree: InterestDegree
    book_id: UUID
    user_id: UUID

    @model_validator(mode='after')
    def verify_object(self):
        if self.book_id == self.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Book_id and user_id are wrong'
            )
        return self


class UserInterestUpdate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    degree: InterestDegree