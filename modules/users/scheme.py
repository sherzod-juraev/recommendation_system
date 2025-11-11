from datetime import datetime
from re import match
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class UserOut(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    username: str
    email: str
    full_name: str | None = None
    created_at: datetime


class UserIn(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    username: str = Field(max_length=25)
    password: str = Field(max_length=30)

    @field_validator('username')
    def verify_username(cls, value):
        pattern = r'^[A-Za-z]{1}[A-Za-z\d]{1,25}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Username invalid'
            )

    @field_validator('password')
    def verify_password(cls, value):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{1,30}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Password invalid'
            )
