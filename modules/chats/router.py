from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from core import verify_access_token
from database import get_db
from . import Chat, ChatIn, ChatOut, crud


chat_router = APIRouter()


@chat_router.post(
    '/',
    summary='Create chat',
    status_code=status.HTTP_201_CREATED,
    response_model=ChatOut
)
async def create_chat(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        chat_scheme: ChatIn,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Chat:
    chat_db = await crud.create_chat(db, chat_scheme, user_id)
    return chat_db


@chat_router.delete(
    '/{chat_id}',
    summary='Delete chat',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    dependencies=[Depends(verify_access_token)]
)
async def delete_chat(
        chat_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_chat(db, chat_id)


@chat_router.get(
    '/',
    summary='Get chats by user_id',
    status_code=status.HTTP_200_OK,
    response_model=list[ChatOut]
)
async def get_chats(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        db: Annotated[AsyncSession, Depends(get_db)],
        skip: int = 0,
        limit: int = 10
) -> list[Chat]:
    chats_list = await crud.verify_chat_by_user_id(db, user_id, skip, limit)
    return chats_list