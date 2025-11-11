from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, Response, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from core import verify_access_token, verify_refresh_token, create_access_token, create_refresh_token, settings
from database import get_db
from . import User, UserIn, UserUpdate, UserOut, Token, crud


user_router = APIRouter()


@user_router.post(
    '/sign/in',
    summary='Create user',
    status_code=status.HTTP_201_CREATED,
    response_model=Token
)
async def create_user(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Token:
    user_scheme = UserIn(
        username=form_data.username,
        password=form_data.password
    )
    user_db = await crud.create_user(db, user_scheme)
    response.set_cookie(
        key='refresh_token',
        value=create_refresh_token(user_db.id),
        max_age=60 * 60 * 24 *  settings.refresh_token_days,
        expires=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days),
        httponly=True
    )
    token = Token(
        access_token=create_access_token(user_db.id)
    )
    return token


@user_router.post(
    '/refresh',
    summary='access_token and refresh update by refresh_token',
    status_code=status.HTTP_200_OK,
    response_model=Token
)
async def update_token(
        request: Request,
        response: Response
) -> Token:
    refresh_token = request.cookies.get('refresh_token')
    user_id = verify_refresh_token(refresh_token)
    response.set_cookie(
        key='refresh_token',
        value=create_refresh_token(user_id),
        max_age=60 * 60 * 24 * settings.refresh_token_days,
        expires=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days),
        httponly=True
    )
    token = Token(
        access_token=create_access_token(user_id)
    )
    return token


@user_router.put(
    '/',
    summary='User full update',
    status_code=status.HTTP_200_OK,
    response_model=UserOut
)
async def full_update(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        user_scheme: UserUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_db = await crud.update_user(db, user_scheme, user_id)
    return user_db


@user_router.patch(
    '/',
    summary='User partial update',
    status_code=status.HTTP_200_OK,
    response_model=UserOut
)
async def partial_update(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        user_scheme: UserUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_db = await crud.update_user(db, user_scheme, user_id, True)
    return user_db


@user_router.delete(
    '/',
    summary='Delete user',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_user(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        user_scheme: UserIn,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_user(db, user_scheme, user_id)


@user_router.get(
    '/',
    summary='Get user',
    status_code=status.HTTP_200_OK,
    response_model=UserOut
)
async def get_user(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_db = await crud.verify_user(db, user_id)
    return user_db