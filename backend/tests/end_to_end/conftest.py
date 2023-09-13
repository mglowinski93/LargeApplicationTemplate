import pytest


from apps.common.database import Base
from bootstrap import create_app, close_application_cleanup


@pytest.fixture(scope="module")
def app():
    yield create_app(environment_name="test")
    close_application_cleanup()


@pytest.fixture
def client(app, prepared_database):
    Base.metadata.create_all(
        prepared_database
    )  # Create the schema in the test database.

    yield app.test_client()

    Base.metadata.drop_all(prepared_database)  # Drop the schema from the test database.
