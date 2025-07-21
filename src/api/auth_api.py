from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.api.common import ApiResponse
from src.entity import Token, UserCreate
from src.repository import user as user_repository
from src.utils import create_access_token

auth_route: APIRouter = APIRouter(prefix="/auth", tags=["auth"])


@auth_route.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()) -> ApiResponse[Token]:
    if await user_repository.verify_user_password(
        email=form_data.username, password=form_data.password
    ):
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return ApiResponse.success(
            "login success", Token(access_token=access_token, token_type="bearer")
        )
    return ApiResponse.fail("login failed", False)


@auth_route.post(path="/register")
async def register(user: UserCreate) -> ApiResponse:
    await user_repository.create_user(user)
    return ApiResponse.success("register success")
