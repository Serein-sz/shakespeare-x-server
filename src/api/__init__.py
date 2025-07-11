from fastapi import FastAPI
from .user_api import user_route
from .auth_api import auth_route


def register_route(app: FastAPI):
    app.include_router(user_route)
    app.include_router(auth_route)

__all__ = ["register_route"]
