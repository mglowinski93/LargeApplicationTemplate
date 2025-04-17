import celery
import pytest
from flask import Flask

from bootstrap import close_app_cleanup, create_app
from modules.common.adapters.notifications.notificators import DummyEmailNotificator
from modules.common.database import Base

from ..common import annotations
from ..dtos import APIClientData


@pytest.fixture(scope="module")
def app() -> annotations.YieldFixture[Flask]:
    yield create_app(environment_name="test")
    close_app_cleanup()


@pytest.fixture
def client(app, prepared_database) -> annotations.YieldFixture[APIClientData]:
    Base.metadata.create_all(prepared_database)
    yield APIClientData(app.test_client())
    Base.metadata.drop_all(prepared_database)


# Mocking Celery worker.
# More details can be found here:
# https://docs.celeryq.dev/en/stable/userguide/testing.html#celery-worker-embed-live-worker.
@pytest.fixture(scope="session", autouse=True)
def task_dispatcher() -> annotations.YieldFixture:
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


@pytest.fixture(autouse=True)
def reset_dummy_email_notificator() -> annotations.YieldFixture[None]:
    DummyEmailNotificator.total_emails_sent = 0
    yield
    DummyEmailNotificator.total_emails_sent = 0
