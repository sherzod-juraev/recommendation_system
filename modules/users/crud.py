from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID
from . import User, UserIn, UserUpdate
from core import hashed_pass, verify_password


async def save_to_db(
        db: AsyncSession,
        user_db: User,
        /
) -> User:
    try:
        await db.commit()
        await db.refresh(user_db)
        return user_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg =  str(exc.orig)
        if 'ix_users_username' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already exists'
            )
        elif 'users_email_key' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already exists'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating user'
        )


async def create_user(
        db: AsyncSession,
        user_scheme: UserIn,
        /
) -> User:
    user_db = User(
        username=user_scheme.username,
        password=hashed_pass(user_scheme.password)
    )
    db.add(user_db)
    user_db = await save_to_db(db, user_db)
    return user_db


async def update_user(
        db: AsyncSession,
        user_scheme: UserUpdate,
        user_id: UUID,
        exclude_unset: bool = False,
        /
) -> User:
    user_db = await verify_user(db, user_id)
    for field, value in user_scheme.model_dump(exclude_unset=exclude_unset).items():
        if field != 'password':
            setattr(user_db, field, value)
        else:
            setattr(user_db, field, hashed_pass(value))
    user_db = await save_to_db(db, user_db)
    return user_db


async def verify_user(
        db: AsyncSession,
        user_id: UUID,
        /
) -> User:
    user_db = await db.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user_db


async def verify_username_password(
        user_db: User,
        user_scheme: UserIn,
        /
) -> None:
    username = user_db.username == user_scheme.username
    password = verify_password(user_scheme.password, user_db.password)
    if not username and not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username and password are wrong'
        )
    elif not username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username is wrong'
        )
    elif not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Password is wrong'
        )


async def delete_user(
        db: AsyncSession,
        user_scheme: UserIn,
        user_id: UUID,
        /
) -> None:
    user_db = await verify_user(db, user_id)
    await verify_username_password(user_db, user_scheme)
    await db.delete(user_db)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error deleting user'
        )