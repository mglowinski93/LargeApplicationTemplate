import pytest
from bootstrap import create_app


@pytest.fixture(scope="session")
def app():
    yield create_app(environment_name="test")


@pytest.fixture
def client(app):
    yield app.test_client()
