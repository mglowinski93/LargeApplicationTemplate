from typing import Optional

from sqlalchemy import (
    create_engine,
    MetaData,
)
from sqlalchemy.orm import sessionmaker, registry, Session


session: Optional[Session] = None


def initialize_database(database_url: str):
    global session

    session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=create_engine(
            url=database_url,
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=100,
        ),
    )()


def get_session() -> Session:
    if session is None:
        raise RuntimeError("Database session not initialized.")

    return session


metadata = MetaData()
mapper_registry = registry()
