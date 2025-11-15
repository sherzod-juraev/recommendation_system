from fastapi import APIRouter


# import routers
from .related_genres.router import genre_relation_router
from .user_interests.router import user_interest_router


learn_router = APIRouter()


learn_router.include_router(
    genre_relation_router,
    prefix='/genre-relation',
    tags=['Genre relation']
)

learn_router.include_router(
    user_interest_router,
    prefix='/userinterest',
    tags=['User interest']
)