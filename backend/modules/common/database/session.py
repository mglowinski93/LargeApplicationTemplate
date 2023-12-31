from typing import Optional

from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import sessionmaker, Session


session: Optional[Session] = None


def initialize_database(database_url: str):
    global session

    # It's important to keep data consistent between transactions and
    # avoid race conditions.
    # In this approach, "REPEATABLE READ" isolation level is used.
    # More details can be found here:
    # https://www.postgresql.org/docs/12/transaction-iso.html.
    # This approach is related to SQL, not strictly to PostgreSQL.

    # A few solutions for handling data consistency are described here:
    # https://www.cosmicpython.com/book/chapter_07_aggregate.html.

    session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=create_engine(
            url=database_url,
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=100,
            isolation_level="REPEATABLE READ",
        ),
    )()


def get_session() -> Session:
    if session is None:
        raise RuntimeError("Database session not initialized.")

    return session
