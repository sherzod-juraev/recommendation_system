from datetime import datetime
from re import match
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator, EmailStr
from uuid import UUID


class Token(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    access_token: str
    token_type: str = 'bearer'


class UserOut(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    username: str
    email: str | None = None
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
        pattern = r'^[A-Za-z]{1}[A-Za-z\d_]{1,25}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Username invalid'
            )
        return value


    @field_validator('password')
    def verify_password(cls, value):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{1,30}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Password invalid'
            )
        return value


class UserUpdate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    username: str | None = Field(None, max_length=25)
    password: str | None = Field(None, max_length=30)
    email: EmailStr | None = Field(None, max_length=250)
    full_name: str | None = Field(None, max_length=100)

    @field_validator('username')
    def verify_username(cls, value):
        pattern = r'^[A-Za-z]{1}[A-Za-z\d_]{1,25}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Username invalid'
            )
        return value


    @field_validator('password')
    def verify_password(cls, value):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{1,30}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Password invalid'
            )
        return value


    @field_validator('full_name')
    def verify_full_name(cls, value):
        pattern = r'^[A-Za-z ]{1,100}$'
        if not match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Full name invalid'
            )
        return value