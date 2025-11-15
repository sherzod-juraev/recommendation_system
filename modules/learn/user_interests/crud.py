from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from . import UserInterest, UserInterestIn, UserInterestUpdate


async def save_to_db(
        db: AsyncSession,
        user_interest_db: UserInterest,
        /
) -> UserInterest:
    try:
        await db.commit()
        await db.refresh(user_interest_db)
        return user_interest_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'user_interests_book_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Book not found'
            )
        elif 'user_interests_user_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User not found'
            )


async def create_user_interest(
        db: AsyncSession,
        user_interest_scheme: UserInterestIn,
        user_id: UUID,
        /
) -> UserInterest:
    user_interest_db = UserInterest(
        degree=user_interest_scheme.degree,
        book_id=user_interest_scheme.book_id,
        user_id=user_id
    )
    db.add(user_interest_db)
    user_interest_db = await save_to_db(db, user_interest_db)
    return user_interest_db


async def update_user_interest(
        db: AsyncSession,
        user_interest_scheme: UserInterestUpdate,
        user_interest_id: UUID,
        exclude_unset: bool = False,
        /
) -> UserInterest:
    user_interest_db = await verify_user_interest(db, user_interest_id)
    for field, value in user_interest_scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(user_interest_db, field, value)
    user_interest_db = await save_to_db(db, user_interest_db)
    return user_interest_db


async def delete_user_interest(
        db: AsyncSession,
        user_interest_id: UUID,
        /
) -> None:
    user_interest_db = await verify_user_interest(db, user_interest_id)
    await db.delete(user_interest_db)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error deleting user_interest'
        )


async def verify_user_interest(
        db: AsyncSession,
        user_interest_id: UUID,
        /
) -> UserInterest:
    user_interest_db = await db.get(UserInterest, user_interest_id)
    if not user_interest_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User interest not found'
        )
    return user_interest_db