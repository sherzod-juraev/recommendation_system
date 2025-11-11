from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
from fastapi import HTTPException, status
from uuid import UUID
from . import Chat, ChatIn


async def save_to_db(
        db: AsyncSession,
        chat_db: Chat,
        /
) -> Chat:
    try:
        await db.commit()
        await db.refresh(chat_db)
        return chat_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'chats_user_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating chat'
        )


async def create_chat(
        db: AsyncSession,
        chat_scheme: ChatIn,
        user_id: UUID,
        /
) -> Chat:
    chat_db = Chat(
        title=chat_scheme.title,
        user_id=user_id
    )
    db.add(chat_db)
    chat_db = await save_to_db(db, chat_db)
    return chat_db


async def verify_chat_by_user_id(
        db: AsyncSession,
        user_id: UUID,
        skip: int,
        limit: int,
        /
) -> list[Chat]:
    query = select(Chat).where(Chat.user_id == user_id).order_by(Chat.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    chats_list = result.scalars().all()
    if not chats_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chats not found'
        )
    return chats_list


async def delete_chat(
        db: AsyncSession,
        chat_id: UUID,
        /
) -> None:
    query = delete(Chat).where(Chat.id == chat_id)
    result = await db.execute(query)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chat not found'
        )