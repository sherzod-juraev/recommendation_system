from fastapi import APIRouter

# import routers
from .users.router import user_router
from .chats.router import chat_router
from .contents.router import content_router
from .recommendation import recommendation_router

# import models
from .users import User
from .chats import Chat
from .contents import Content
from .recommendation.authors import Author
from .recommendation.genres import Genre


__all__ = ['User', 'Chat', 'Content', 'Author', 'Genre']


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

api_router.include_router(
    recommendation_router
)