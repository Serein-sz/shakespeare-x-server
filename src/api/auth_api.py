from fastapi import APIRouter
from src.entity import UserLoginRequest
from src.repository import user as user_repository
from .common import ApiResponse

auth_route = APIRouter(prefix="/auth", tags=["认证"])

@auth_route.post("/login")
async def login(user_login: UserLoginRequest):
    if user_repository.verify_user_password(user_login.email, user_login.password):
        return ApiResponse.fail("login failed")
    return ApiResponse.success("login success")
