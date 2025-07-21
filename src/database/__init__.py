from types import ModuleType


from _frozen_importlib import ModuleSpec


import os
import importlib.util
from datetime import datetime

from sqlalchemy import event

from .db import engine, Session, generator, Base, Model


def load_models() -> None:
    """动态加载所有实体"""
    models_dir: str = os.path.join(os.path.dirname(__file__), "..", "entity")

    for file in os.listdir(models_dir):
        if file.endswith(".py") and file != "__init__.py":
            module_name: str = file[:-3]
            module_path: str = os.path.join(models_dir, file)

            spec: ModuleSpec | None = importlib.util.spec_from_file_location(
                module_name, module_path
            )
            module: ModuleType = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

    # 注册创建时间事件
    @event.listens_for(Model, "before_insert")
    def set_created_at(mapper, connection, target) -> None:
        if hasattr(target, "created_at") and not target.created_at:
            target.created_at = datetime.now()

    # 注册更新时间事件
    @event.listens_for(Model, "before_update")
    def set_updated_at(mapper, connection, target) -> None:
        if hasattr(target, "updated_at"):
            target.updated_at = datetime.now()


# 在初始化数据库时调用
async def init_db() -> None:
    load_models()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


__all__ = ["init_db", "Base", "Session", "generator", "Model"]
