from pydantic import BaseModel
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


class UserInterestUpdate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    degree: InterestDegree