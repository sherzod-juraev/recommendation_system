from fastapi import FastAPI
from core import register_exception_handler

# import api router
from modules import api_router

app = FastAPI()

app.include_router(api_router)
# exception handlers
register_exception_handler(app)