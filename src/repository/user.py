from sqlalchemy import select
from src.database import Session
from src.entity import User, UserCreate, UserUpdate
from src.utils import verify_password


async def create_user(user: UserCreate) -> None:
    async with Session() as session:
        session.add_all([User.from_create(user)])
        await session.commit()


async def update_user(user: UserUpdate) -> None:
    async with Session() as session:
        old: User = await session.get(User, user.id)
        if old:
            old = old.from_update(user)
            await session.commit()


async def delete_user(id: str) -> None:
    async with Session() as session:
        user = await session.get(User, id)
        if user:
            session.delete(user)
            await session.commit()


async def get_user_by_email(email: str) -> User | None:
    async with Session() as session:
        result = await session.execute(select(User).filter(User.email == email))
        return result.scalar()


async def verify_user_password(email: str, password: str) -> bool:
    async with Session() as session:
        # user = await session.query(User).filter(User.email == email).first()
        result = await session.execute(select(User).filter(User.email == email))
        user = result.scalar()
        if user:
            return verify_password(password, user.password)
    return False
