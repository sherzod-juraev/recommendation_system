from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException, status
from uuid import UUID
from . import Content, ContentIn


async def save_to_db(
        db: AsyncSession,
        content_db: Content,
        /
) -> Content:
    try:
        await db.commit()
        await db.refresh(content_db)
        return content_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'contents_chat_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Chat not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating content'
        )


async def create_content(
        db: AsyncSession,
        content_scheme: ContentIn,
        /
) -> Content:
    content_db = Content(
        sender=content_scheme.sender,
        text=content_scheme.text,
        data=content_scheme.data,
        chat_id=content_scheme.chat_id
    )
    db.add(content_db)
    content_db = await save_to_db(db, content_db)
    return content_db


async def verify_contents_by_chat_id(
        db: AsyncSession,
        chat_id: UUID,
        /
) -> list[Content]:
    query = select(Content).where(Content.chat_id == chat_id).order_by(Content.created_at.asc())
    result = await db.execute(query)
    contents_list = result.scalars().all()
    if not contents_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Contents not found'
        )
    return contents_list