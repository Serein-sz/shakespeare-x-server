from fastapi import FastAPI, Depends

from src.dependencies import get_current_user
from .auth_api import auth_route
from .user_api import user_route


def register_route(app: FastAPI) -> None:
    app.include_router(auth_route)
    app.include_router(user_route, dependencies=[Depends(get_current_user)])


__all__ = ["register_route"]
