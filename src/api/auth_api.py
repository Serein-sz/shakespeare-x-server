from fastapi import APIRouter

from src.entity import UserLoginRequest

from src.repository import user as user_repository

from .common import ApiResponse

auth_route: APIRouter = APIRouter(prefix="/auth", tags=["认证"])


@auth_route.post(path="/login")
async def login(user_login: UserLoginRequest) -> ApiResponse:
    if user_repository.verify_user_password(
        email=user_login.email, password=user_login.password
    ):
        return ApiResponse.fail("login failed")
    return ApiResponse.success("login success")
