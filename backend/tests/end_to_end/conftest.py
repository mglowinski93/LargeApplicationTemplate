import pytest
from bootstrap import create_app

from apps.common.database.session import metadata
from apps.template_app.adapters.repositories.sqlalchemy.orm import (
    clear_mappers as clear_template_mappers,
)


@pytest.fixture(scope="session")
def app():
    yield create_app(environment_name="test")
    clear_template_mappers()


@pytest.fixture
def client(app, prepared_database):
    metadata.create_all(prepared_database)  # Create the schema in the test database.

    yield app.test_client()

    metadata.drop_all(prepared_database)  # Drop the schema from the test database.
