import logging
import os
from typing import Callable

from celery import Celery

from ...domain import ports

logger = logging.getLogger(__name__)


task_dispatcher = Celery(
    main="celery-task-dispatcher",
    broker=os.environ["BROKER_URL"],
    broker_connection_retry_on_startup=True,
    accept_content=("application/x-python-serialize",),
)


@task_dispatcher.task
def _task(func, *args, **kwargs):
    return func(*args, **kwargs)


class CeleryTaskDispatcher(ports.AbstractTaskDispatcher):
    @staticmethod
    def dispatch(func: Callable, *args, **kwargs) -> None:
        _task.apply_async(args=(func, *args), kwargs=kwargs, serializer="pickle")
