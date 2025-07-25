from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependencies import get_current_user
from src.entity import User, UserUpdate
from src.entity.user import UserVo
from src.repository import user as user_repository

from .common import ApiResponse

user_route: APIRouter = APIRouter(prefix="/user", tags=["user"])


@user_route.put("/")
async def update_user(user: UserUpdate) -> ApiResponse:
    await user_repository.update_user(user)
    return ApiResponse.success("user update success")


@user_route.delete("/{id}")
async def delete_user(id: str) -> ApiResponse:
    await user_repository.delete_user(id)
    return ApiResponse.success("user delete success")


@user_route.get("/")
async def get_user(
    user: Annotated[User, Depends(get_current_user)],
) -> ApiResponse[UserVo]:
    return ApiResponse.success("user get success", data=user.to_user_vo())
