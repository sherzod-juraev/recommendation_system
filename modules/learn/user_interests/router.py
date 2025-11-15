from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from core import verify_access_token
from database import get_db
from . import UserInterest, UserInterestIn, UserInterestUpdate, UserInterestOut, crud


user_interest_router = APIRouter()


@user_interest_router.post(
    '/',
    summary='Create user interest',
    status_code=status.HTTP_201_CREATED,
    response_model=UserInterestOut
)
async def create_user_interest(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        user_interest_scheme: UserInterestIn,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> UserInterest:
    user_interest_db = await crud.create_user_interest(db, user_interest_scheme, user_id)
    return user_interest_db


@user_interest_router.patch(
    '/{user_interest_id}',
    summary='User interest partial update',
    status_code=status.HTTP_200_OK,
    response_model=UserInterestOut,
    dependencies=[Depends(verify_access_token)]
)
async def partial_update(
        user_interest_id: UUID,
        user_interest_scheme: UserInterestUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> UserInterest:
    user_interest_db = await crud.update_user_interest(db, user_interest_scheme, user_interest_id, True)
    return user_interest_db


@user_interest_router.delete(
    '/{user_interest_id}',
    summary='Delete user interest',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    dependencies=[Depends(verify_access_token)]
)
async def delete_user_interest(
        user_interest_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_user_interest(db, user_interest_id)


@user_interest_router.get(
    '/{user_interest_id}',
    summary='Get user interest by id',
    status_code=status.HTTP_200_OK,
    response_model=UserInterestOut,
    dependencies=[Depends(verify_access_token)]
)
async def get_user_interest(
        user_interest_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> UserInterest:
    user_interest_db = await crud.verify_user_interest(db, user_interest_id)
    return user_interest_db