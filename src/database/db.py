from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine


from sqlalchemy.orm import Mapped, declarative_base, sessionmaker
from snowflake import SnowflakeGenerator

Base = declarative_base()

# 创建引擎
engine: AsyncEngine = create_async_engine(
    "mysql+aiomysql://root:Caonima3344@112.125.89.224:3308/shakespeare-x",
    echo=True,  # 输出SQL日志
    future=True,  # 使用2.0风格API
    pool_size=5,  # 连接池大小
    max_overflow=10,  # 允许超出连接池的连接数
    pool_timeout=30,  # 获取连接超时时间(秒)
)


Session: sessionmaker[AsyncSession] = sessionmaker[AsyncSession](
    bind=engine, class_=AsyncSession, future=True
)

generator: SnowflakeGenerator = SnowflakeGenerator(0)


class TimestampMixin:
    """时间戳混合类"""

    created_at: Mapped[datetime] = Column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = Column[datetime](
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )


class Model(Base, TimestampMixin):
    """所有模型的基类"""

    __abstract__ = True
