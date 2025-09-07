from typing import Any, Generator

from config import settings
from sqlmodel import Session, SQLModel, create_engine

postgres_url = settings.POSTGRES_URL
engine = create_engine(postgres_url, echo=True)
SQLModel.metadata.create_all(engine)


def get_db_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
