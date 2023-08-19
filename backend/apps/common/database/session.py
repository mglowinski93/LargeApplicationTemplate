import os
from contextlib import contextmanager

from sqlalchemy import (
    create_engine,
    MetaData,
)
from sqlalchemy.orm import sessionmaker, registry


DATABASE_URL = (f"postgresql://"
                f"{os.environ['POSTGRES_DB_USER']}:{os.environ['POSTGRES_DB_PASSWORD']}"
                f"@"
                f"{os.environ['POSTGRES_DB_HOST']}:{os.environ['POSTGRES_DB_PORT']}"
                f"/{os.environ['POSTGRES_DB_NAME']}")

engine = create_engine(
    url=DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=100,
)
metadata = MetaData()
mapper_registry = registry()


def get_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()


@contextmanager
def session_scope():
    session = get_session()

    try:
        yield session
        session.commit()
        session.flush()
    except Exception as err:
        session.rollback()
        raise err from err
    finally:
        session.close()
