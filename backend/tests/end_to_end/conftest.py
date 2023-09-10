import pytest


@pytest.fixture(scope="session")
def app():
    pass


@pytest.fixture
def client(app, prepared_database):
    pass
