from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SESSION: Session | None = None


def initialize_database_sessions(
    database_url: str,
):
    global SESSION

    # It's important to keep data consistent between transactions and
    # avoid race conditions.
    # In this approach, "REPEATABLE READ" isolation level is used.
    # More details can be found here:
    # https://www.postgresql.org/docs/12/transaction-iso.html.
    # This approach is related to SQL, not strictly to PostgreSQL.

    # A few solutions for handling data consistency are described here:
    # https://www.cosmicpython.com/book/chapter_07_aggregate.html.

    SESSION = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=create_engine(
            url=database_url,
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=100,
            isolation_level="REPEATABLE READ",
            # Each PostreSQL connection has an associated time zone that defaults to
            # system's time zone, so it has to be manually set to UTC
            # in order to support multiple timezones.
            # More details can be found here:
            # https://stackoverflow.com/questions/26105730/sqlalchemy-converting-utc-datetime-to-local-time-before-saving.
            connect_args={"options": "-c timezone=utc"},
        ),
    )()


def get_session() -> Session:
    if SESSION is None:
        raise RuntimeError("Database session not initialized.")

    return SESSION
