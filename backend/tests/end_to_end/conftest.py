import pytest
from bootstrap import create_app

from apps.common.database.session import metadata


@pytest.fixture(scope="class")
def app():
    yield create_app(environment_name="test")


@pytest.fixture
def client(app, prepared_database):
    metadata.create_all(prepared_database)  # Create the schema in the test database.

    yield app.test_client()

    metadata.drop_all(prepared_database)  # Drop the schema from the test database.
