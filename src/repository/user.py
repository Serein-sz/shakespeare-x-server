from src.database import Session
from src.entity import User, UserCreate, UserUpdate
from src.utils import verify_password


def create_user(user: UserCreate) -> None:
    with Session() as session:
        session.add_all([User.from_create(user)])
        session.commit()


def update_user(user: UserUpdate) -> None:
    with Session() as session:
        old: User = session.get(User, user.id)
        if old:
            old = old.from_update(user)
            session.commit()


def delete_user(id: str) -> None:
    with Session() as session:
        user = session.get(User, id)
        if user:
            session.delete(user)
            session.commit()

def get_user_by_email(email: str) -> User | None:
    with Session() as session:
        return session.query(User).filter(User.email == email).first()

def verify_user_password(email: str, password: str) -> bool:
    with Session() as session:
        user = session.query(User).filter(User.email == email).first()
        if user:
            return verify_password(password, user.password)
    return False
