from fastapi import APIRouter
from .response import response_router

brain_router = APIRouter()


brain_router.include_router(
    response_router,
    prefix='/response',
    tags=['Response']
)