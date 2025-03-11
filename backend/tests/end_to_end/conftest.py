import celery
import pytest

from bootstrap import close_app_cleanup, create_app
from modules.common.database import Base

from ..common.annotations import YieldFixture


@pytest.fixture(scope="module")
def app():
    yield create_app(environment_name="test")
    close_app_cleanup()


@pytest.fixture
def client(app, prepared_database):
    Base.metadata.create_all(prepared_database)
    yield app.test_client()
    Base.metadata.drop_all(prepared_database)


# Mocking Celery worker.
# More details can be found here:
# https://docs.celeryq.dev/en/stable/userguide/testing.html#celery-worker-embed-live-worker.
@pytest.fixture(scope="session", autouse=True)
def task_dispatcher() -> YieldFixture:
    """
    Mocks a Celery worker to run tasks synchronously.

    By setting `task_always_eager` to `True`,
    tasks will run immediately rather than on a worker.
    """

    key = "task_always_eager"
    pre_eager = celery.app.defaults.DEFAULTS[key]

    celery.app.defaults.DEFAULTS[key] = True
    yield
    celery.app.defaults.DEFAULTS[key] = pre_eager
