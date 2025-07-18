from fastapi import APIRouter
from src.repository import user as user_repository
from src.entity import UserUpdate
from .common import ApiResponse

user_route: APIRouter = APIRouter(prefix="/user", tags=["user"])


@user_route.put("/")
async def update_user(user: UserUpdate) -> ApiResponse:
    user_repository.update_user(user)
    return ApiResponse.success("user update success")


@user_route.delete("/{id}")
async def delete_user(id: str) -> ApiResponse:
    user_repository.delete_user(id)
    return ApiResponse.success("user delete success")
