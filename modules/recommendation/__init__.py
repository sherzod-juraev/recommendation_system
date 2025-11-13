from fastapi import APIRouter

# import nested router
from .authors.router import author_router


recommendation_router = APIRouter()


recommendation_router.include_router(
    author_router,
    prefix='/author',
    tags=['Authors']
)