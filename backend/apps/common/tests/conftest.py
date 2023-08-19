import os

import pytest
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from apps.common.database.session import DATABASE_URL


TEST_DATABASE_URL = f"{DATABASE_URL}_test"


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        url=TEST_DATABASE_URL,
        pool_pre_ping=True,
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def prepared_database(db_engine):
    with DatabaseJanitor(
        user=os.environ["POSTGRES_DB_USER"],
        password=os.environ["POSTGRES_DB_PASSWORD"],
        host=os.environ["POSTGRES_DB_HOST"],
        port=os.environ["POSTGRES_DB_PORT"],
        dbname=TEST_DATABASE_URL.rsplit(sep="/", maxsplit=1)[1],
        version="",
    ):
        yield db_engine


@pytest.fixture
def raw_db_session(  # <- This is the fixture to be used in tests.
    prepared_database,
):
    with prepared_database.connect() as db_connection:
        transaction = db_connection.begin()
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
        session.configure(bind=db_connection)

        yield session()

        session.remove()
        transaction.rollback()
