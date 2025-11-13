from fastapi import APIRouter

# import nested router
from .authors.router import author_router
from .genres.router import genre_router
from .books.router import book_router


recommendation_router = APIRouter()


recommendation_router.include_router(
    author_router,
    prefix='/author',
    tags=['Authors']
)

recommendation_router.include_router(
    genre_router,
    prefix='/genre',
    tags=['Genres']
)

recommendation_router.include_router(
    book_router,
    prefix='/book',
    tags=['Books']
)