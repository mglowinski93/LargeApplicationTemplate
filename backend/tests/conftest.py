from typing import Callable

import inject
import pytest
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from modules.common.database import Base
from modules.common import message_bus as common_message_bus
from modules.template_module.domain import commands as template_domain_commands
from modules.template_module.domain import events as template_domain_events
from config import config
from modules.template_module.domain.entities import Template as TemplateEntity
from . import fakers
from .common import annotations


configuration = config["test"]()


@pytest.fixture(scope="session")
def db_engine() -> annotations.YieldFixture[Engine]:
    engine = create_engine(
        url=configuration.database_url,
        pool_pre_ping=True,
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="module")
def prepared_database(db_engine) -> annotations.YieldFixture[Engine]:
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
) -> annotations.YieldFixture[Session]:
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
def db_session(raw_db_session) -> annotations.YieldFixture[Session]:
    # Add here logic responsible for additional ORM configuration
    # e.g. mappers setup: https://docs.sqlalchemy.org/en/13/orm/mapping_styles.html#classical-mappings.

    yield raw_db_session


@pytest.fixture
def db_session_factory(db_session) -> Callable:
    def db_session_():
        return db_session

    return db_session_


@pytest.fixture
def fake_main_task_dispatcher_inject():
    fake_task_dispatcher_instance = fakers.FakeTaskDispatcher()

    inject.clear_and_configure(
        lambda binder: binder.bind(
            "main_task_dispatcher", fake_task_dispatcher_instance
        )
    )

    yield fake_task_dispatcher_instance

    inject.clear()


@pytest.fixture
def message_bus() -> annotations.YieldFixture[common_message_bus.MessageBus]:
    yield common_message_bus.MessageBus(
        event_handlers={
            template_domain_events.TemplateCreated: [],
            template_domain_events.TemplateDeleted: [],
            template_domain_events.TemplateValueSet: [],
        },
        command_handlers={
            template_domain_commands.CreateTemplate: lambda event: None,
            template_domain_commands.DeleteTemplate: lambda event: None,
            template_domain_commands.SetTemplateValue: lambda event: None,
        },
    )


@pytest.fixture
def fake_template_unit_of_work_factory() -> Callable:
    def fake_unit_of_work(
        initial_templates: list[TemplateEntity] = [],
    ) -> fakers.FakeTemplateUnitOfWork:
        return fakers.FakeTemplateUnitOfWork(
            templates=initial_templates if initial_templates else []
        )

    return fake_unit_of_work
