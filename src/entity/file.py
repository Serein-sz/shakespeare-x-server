from sqlalchemy import Column, String, Text, ForeignKey
from pydantic import BaseModel
from typing import Optional, List, Literal

from src.database import Model, generator


class FileTree(BaseModel):
    """
    树节点模型

    作者: 王强
    日期: 2025-07-21
    版本: 1.1.0
    """

    id: Optional[str] = None
    name: str
    parent_id: Optional[str] = None
    type: Literal["folder", "file"]
    content: Optional[str] = None
    user_id: str


class FileTreeCreate(FileTree):
    """创建树节点模型"""

    user_id: Optional[str] = None


class FileTreeUpdate(FileTree):
    """更新树节点模型"""

    id: str


class FileTreeUpdateContent(BaseModel):
    """更新节点内容"""

    id: str
    content: str


class FileTreeVo(FileTree):
    """视图模型"""

    children: Optional[List["FileTree"]] = None


class FileTreeDb(Model):
    """
    树节点数据库模型

    作者: 王强
    日期: 2025-07-21
    版本: 1.1.0
    """

    __tablename__ = "files"
    __table_args__ = {"extend_existing": True}

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(String(50), nullable=True)
    type = Column(String(10), nullable=False)  # 'folder' or 'file'
    content = Column(Text, nullable=True)
    user_id = Column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"<FileTree(id={self.id}, name='{self.name}', type='{self.type}')>"

    @classmethod
    def from_create(cls, node_create: FileTreeCreate) -> "FileTreeDb":
        """从创建模型转换为数据库模型"""
        node = cls(**node_create.model_dump(exclude_unset=True))
        node.id = next(generator)
        return node

    def from_update(self, node_update: FileTreeUpdate) -> "FileTreeDb":
        """从更新模型更新数据库模型"""
        for field, value in node_update.model_dump(exclude_unset=True).items():
            if hasattr(self, field):
                setattr(self, field, value)
        return self

    def to_tree_node_vo(self) -> FileTreeVo:
        """转换为视图模型"""
        return FileTreeVo(
            id=self.id,
            name=self.name,
            parent_id=self.parent_id,
            type=self.type,
            content=self.content,
            user_id=self.user_id,
        )
