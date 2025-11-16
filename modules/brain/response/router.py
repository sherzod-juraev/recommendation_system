from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database import get_db
from core import verify_access_token
from ...recommendation.books import BookOut, Book
from .hybrid_conclusion import hybrid_conclusion


response_router = APIRouter()


@response_router.get(
    '/',
    summary='Recommend new books',
    status_code=status.HTTP_200_OK,
    response_model=list[BookOut]
)
async def get_books(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> list[Book]:
    books_list = await hybrid_conclusion(db, user_id)
    return books_list