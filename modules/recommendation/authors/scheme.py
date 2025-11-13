from re import match
from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator, Field
from uuid import UUID
from ..books import BookOut


class AuthorOut(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    full_name: str
    books: list[BookOut] = []


class AuthorIn(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    full_name: str = Field(max_length=100)


    @field_validator('full_name')
    def  verify_full_name(cls, value):
        pattern = r'^[A-Za-z ]{1,100}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Full name is wrong'
            )
        return value