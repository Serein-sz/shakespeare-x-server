from typing import Annotated

from fastapi import APIRouter, Depends

from src.repository import file as file_repository
from src.entity import (
    User,
    FileTreeCreate,
    FileTreeVo,
    FileTreeUpdateContent,
)
from src.dependencies import get_current_user
from .common import ApiResponse

file_route: APIRouter = APIRouter(prefix="/file", tags=["file"])


@file_route.get("/")
async def get_file(
    user: Annotated[User, Depends(get_current_user)],
) -> ApiResponse[list[FileTreeVo]]:
    files = await file_repository.get_files_vo(user.id)
    return ApiResponse.success("file get success", files)


@file_route.get("/{id}")
async def get_file_content_by_id(id: str) -> ApiResponse[str]:
    content = await file_repository.get_file_content_by_id(id)
    return ApiResponse.success("file get success", content)


@file_route.post("/")
async def create_file(
    file: FileTreeCreate,
    user: Annotated[User, Depends(get_current_user)],
) -> ApiResponse:
    file.user_id = user.id
    await file_repository.create_file(file)
    return ApiResponse.success("file create success")


@file_route.delete("/")
async def delete_file(id: str) -> ApiResponse:
    await file_repository.delete_file(id)
    return ApiResponse.success("file delete success")


@file_route.put("/update-content")
async def update_file(file: FileTreeUpdateContent) -> ApiResponse:
    await file_repository.update_content(file.id, file.content)
    return ApiResponse.success("file update success")
