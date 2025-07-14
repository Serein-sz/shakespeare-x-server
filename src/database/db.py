from datetime import datetime

from sqlalchemy import Engine, create_engine, Column, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from snowflake import SnowflakeGenerator

Base = declarative_base()

# 创建引擎
engine: Engine = create_engine(
    "mysql+pymysql://root:Caonima3344@112.125.89.224:3308/shakespeare-x",
    echo=True,  # 输出SQL日志
    future=True,  # 使用2.0风格API
    pool_size=5,  # 连接池大小
    max_overflow=10,  # 允许超出连接池的连接数
    pool_timeout=30,  # 获取连接超时时间(秒)
)


Session: sessionmaker[Session] = sessionmaker[Session](bind=engine, future=True)

generator: SnowflakeGenerator = SnowflakeGenerator(0)


class TimestampMixin:
    """时间戳混合类"""

    created_at: Column[datetime] = Column[datetime](
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Column[datetime] = Column[datetime](
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )


class Model(Base, TimestampMixin):
    """所有模型的基类"""

    __abstract__ = True
