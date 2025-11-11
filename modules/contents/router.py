from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database import get_db
from . import Content, ContentIn, ContentOut, crud


content_router = APIRouter()


@content_router.post(
    '/',
    summary='Create content',
    status_code=status.HTTP_201_CREATED,
    response_model=ContentOut
)
async def create_content(
        content_scheme: ContentIn,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Content:
    content_db = await crud.create_content(db, content_scheme)
    return content_db


@content_router.get(
    '/{chat_id}',
    summary='Get contents by chat_id',
    status_code=status.HTTP_200_OK,
    response_model=list[ContentOut]
)
async def get_contents(
        chat_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> list[Content]:
    contents_list = await crud.verify_contents_by_chat_id(db, chat_id)
    return contents_list