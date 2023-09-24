import celery
import pytest

from modules.common.database import Base
from bootstrap import create_app, close_app_cleanup


@pytest.fixture(scope="module")
def app():
    yield create_app(environment_name="test")
    close_app_cleanup()


@pytest.fixture
def client(app, prepared_database):
    Base.metadata.create_all(
        prepared_database
    )  # Create the schema in the test database.

    yield app.test_client()

    Base.metadata.drop_all(prepared_database)  # Drop the schema from the test database.


# Mocking Celery worker.
# More details can be found here:
# https://docs.celeryq.dev/en/stable/userguide/testing.html#celery-worker-embed-live-worker.
@pytest.fixture(scope="module")
def task_dispatcher(request):
    """
    Mocks a Celery worker to run tasks synchronously.

    By setting `task_always_eager` to `True`,
    tasks will run immediately rather than on a worker.
    """

    pre_eager = celery.app.defaults.DEFAULTS["task_always_eager"]

    celery.app.defaults.DEFAULTS["task_always_eager"] = True
    yield
    celery.app.defaults.DEFAULTS["task_always_eager"] = pre_eager
