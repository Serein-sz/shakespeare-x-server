import os
import importlib.util
from datetime import datetime

from sqlalchemy import event

from .db import engine, Session, generator, Base, Model



def load_models():
    """动态加载所有模型"""
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'entity')
    
    for file in os.listdir(models_dir):
        if file.endswith('.py') and file != '__init__.py':
            module_name = file[:-3]
            module_path = os.path.join(models_dir, file)
            
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

    # 注册创建时间事件
    @event.listens_for(Model, 'before_insert')
    def set_created_at(mapper, connection, target):
        if hasattr(target, 'created_at') and not target.created_at:
            target.created_at = datetime.now()
    
    # 注册更新时间事件
    @event.listens_for(Model, 'before_update')
    def set_updated_at(mapper, connection, target):
        if hasattr(target, 'updated_at'):
            target.updated_at = datetime.now()

# 在初始化数据库时调用
def init_db():
    load_models()
    Model.metadata.create_all(bind=engine)

__all__ = ["init_db", "Base", "Session", "generator", "Model"]
