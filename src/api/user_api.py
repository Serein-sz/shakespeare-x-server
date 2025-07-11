from fastapi import APIRouter
from src.repository import user as user_repository
from src.entity import UserCreate, UserUpdate
from .common import ApiResponse

user_route = APIRouter(prefix="/user", tags=["用户"])

@user_route.post("/")
async def create_user(user: UserCreate):
    user_repository.create_user(user)
    return ApiResponse.success("user create success")

@user_route.put("/")
async def update_user(user: UserUpdate):
    user_repository.update_user(user)
    return ApiResponse.success("user update success")

@user_route.delete("/{id}")
async def delete_user(id: str):
    user_repository.delete_user(id)
    return ApiResponse.success("user delete success")

