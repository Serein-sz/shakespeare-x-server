import bcrypt
from sqlalchemy import Column, String
from pydantic import BaseModel, EmailStr

from src.database import Model, generator


def hash_password(password: str) -> str:
    """将明文密码转换为 bcrypt 哈希"""
    # 生成盐值并哈希密码
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_bytes.decode("utf-8")  # 转换为字符串存储


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否匹配哈希值"""
    print(plain_password, hashed_password)
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


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
        self.password = hash_password(password)

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


if __name__ == "__main__":
    hashed_password: str = hash_password("123456")
    print(verify_password("123456", hashed_password))
