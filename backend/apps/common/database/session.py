import os

from sqlalchemy import (
    create_engine,
    MetaData,
)
from sqlalchemy.orm import sessionmaker, registry, Session


DATABASE_URL = (
    f"postgresql://"
    f"{os.environ['POSTGRES_DB_USER']}:{os.environ['POSTGRES_DB_PASSWORD']}"
    f"@"
    f"{os.environ['POSTGRES_DB_HOST']}:{os.environ['POSTGRES_DB_PORT']}"
    f"/{os.environ['POSTGRES_DB_NAME']}"
)

engine = create_engine(
    url=DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=100,
)
metadata = MetaData()
mapper_registry = registry()


def get_session() -> Session:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()
