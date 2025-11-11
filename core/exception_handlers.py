from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from sqlalchemy.exc import TimeoutError


def register_exception_handler(app: FastAPI, /) -> None:
    pass