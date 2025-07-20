from fastapi import FastAPI, Depends

from src.dependencies import validate_token
from .auth_api import auth_route
from .user_api import user_route


def register_route(app: FastAPI) -> None:
    app.include_router(auth_route)
    app.include_router(user_route, dependencies=[Depends(validate_token)])


__all__ = ["register_route"]
