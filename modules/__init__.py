from fastapi import APIRouter

# import routers
from .users.router import user_router
from .chats.router import chat_router
from .contents.router import content_router

# import models
from .users import User
from .chats import Chat
from .contents import Content


__all__ = ['User', 'Chat', 'Content']


api_router = APIRouter()

api_router.include_router(
    user_router,
    prefix='/auth',
    tags=['Authenticate']
)

api_router.include_router(
    chat_router,
    prefix='/chats',
    tags=['Chats']
)

api_router.include_router(
    content_router,
    prefix='/content',
    tags=['Contents']
)