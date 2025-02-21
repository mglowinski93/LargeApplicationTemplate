import inject
import pytest
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.common.database import Base
from modules.template_module.domain.entities import Template as TemplateEntity
from config import config
from .factories import TemplateEntityFactory, FakeTaskDispatcher


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
        Base.metadata.create_all(db_engine)  # Create the schema in the test database.

        yield db_engine

        Base.metadata.drop_all(db_engine)  # Drop the schema from the test database.


@pytest.fixture
def raw_db_session(  # < - This is the fixture to be used in tests.
    prepared_database,
):
    with prepared_database.connect() as db_connection:
        transaction = db_connection.begin()
        session = sessionmaker(autocommit=False, autoflush=False, bind=db_connection)()

        yield session

        session.close()
        # Some tests are already rolling back the transaction,
        # so there is a need to check if the transaction is active before rolling back.
        if transaction.is_active:
            transaction.rollback()


@pytest.fixture
def db_session(raw_db_session):
    # Add here logic responsible for additional ORM configuration
    # e.g. mappers setup: https://docs.sqlalchemy.org/en/13/orm/mapping_styles.html#classical-mappings.

    yield raw_db_session


@pytest.fixture
def db_session_factory(db_session):  # noqa: F811
    def db_session_():
        return db_session

    return db_session_


@pytest.fixture
def template_entity() -> TemplateEntity:
    return TemplateEntityFactory.create()  # type: ignore


@pytest.fixture
def fake_main_task_dispatcher_inject():
    fake_task_dispatcher_instance = FakeTaskDispatcher()

    inject.clear_and_configure(
        lambda binder: binder.bind(
            "main_task_dispatcher", fake_task_dispatcher_instance
        )
    )

    yield fake_task_dispatcher_instance

    inject.clear()
