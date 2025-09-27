from typing import Any, Generator

from app.config import settings
from app.models import User
from passlib.context import CryptContext
from sqlmodel import Session, SQLModel, create_engine, select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
postgres_url = settings.POSTGRES_URL
engine = create_engine(postgres_url, echo=True)
SQLModel.metadata.create_all(engine)


def get_db_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_email(*, session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, username: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, username=username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
