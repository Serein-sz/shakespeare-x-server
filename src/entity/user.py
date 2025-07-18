from sqlalchemy import Column, String
from pydantic import BaseModel, EmailStr

from src.database import Model, generator
from src.utils import get_password_hash


class UserDto(BaseModel):
    id: str | None = None
    name: str | None = None
    email: EmailStr


class UserCreate(UserDto):
    password: str


class UserUpdate(UserDto):
    id: str
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class User(Model):
    __tablename__: str = "users"
    __table_args__: dict[str, bool] = {"extend_existing": True}

    id: Column[str] = Column[str](String(50), primary_key=True)
    name: Column[str] = Column[str](String(50), nullable=False)
    password: Column[str] = Column[str](String(100), nullable=False)
    email: Column[str] = Column[str](String(100), unique=True)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

    def set_password(self, password: str) -> None:
        self.password = get_password_hash(password)

    @classmethod
    def from_create(cls, user_create: UserCreate) -> "User":
        user = cls(**user_create.model_dump(exclude_unset=True))
        user.id = next(generator)
        user.set_password(user_create.password)
        return user

    def from_update(self, user_update: UserUpdate) -> "User":
        # 部分更新字段
        for field, value in user_update.model_dump(exclude_unset=True).items():
            if field == "password" and value is not None:
                self.set_password(value)  # 特殊处理密码
            elif hasattr(self, field):
                setattr(self, field, value)
        return self
