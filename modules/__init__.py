from fastapi import APIRouter

# import routers
from .users.router import user_router
from .recommendation import recommendation_router
from .learn import learn_router
from .brain import brain_router

# import models
from .users import User
from .recommendation.authors import Author
from .recommendation.genres import Genre
from .recommendation.books import Book
from .recommendation.book_genres import BookGenre
from .learn.related_genres import GenreRelation
from .learn.user_interests import UserInterest


__all__ = ['User', 'Author', 'Genre', 'Book', 'BookGenre', 'GenreRelation', 'UserInterest']


api_router = APIRouter()

api_router.include_router(
    user_router,
    prefix='/auth',
    tags=['Authenticate']
)

api_router.include_router(
    recommendation_router
)

api_router.include_router(
    learn_router
)

api_router.include_router(
    brain_router
)