import pytest
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apps.common.database.session import metadata
from apps.template_app.domain.entities import Template as TemplateEntity
from config import config
from .factories import TemplateEntityFactory


configuration = config["test"]()


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        url=configuration.database_url,
        pool_pre_ping=True,
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="module")
def prepared_database(db_engine):
    with DatabaseJanitor(
        user=configuration.DATABASE_USER,
        password=configuration.DATABASE_PASSWORD,
        host=configuration.DATABASE_HOST,
        port=configuration.DATABASE_PORT,
        dbname=configuration.DATABASE_NAME,
        version=0,
    ):
        metadata.create_all(db_engine)  # Create the schema in the test database.

        yield db_engine

        metadata.drop_all(db_engine)  # Drop the schema from the test database.


@pytest.fixture
def raw_db_session(  # <- This is the fixture to be used in tests.
    prepared_database,
):
    with prepared_database.connect() as db_connection:
        transaction = db_connection.begin()
        session = sessionmaker(autocommit=False, autoflush=False, bind=db_connection)()

        yield session

        session.close()
        transaction.rollback()


@pytest.fixture
def template_entity() -> TemplateEntity:
    return TemplateEntityFactory()