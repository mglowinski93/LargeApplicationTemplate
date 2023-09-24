import os
import logging

from celery import Celery

from ...domain.ports import TaskDispatcher


logger = logging.getLogger(__name__)


task_dispatcher = Celery(
    main="celery-task-dispatcher",
    broker=os.environ["BROKER_URL"],
    broker_connection_retry_on_startup=True,
)


class CeleryTaskDispatcher(TaskDispatcher):
    @staticmethod
    def send_email(content: str):
        _send_email.delay(content)


@task_dispatcher.task
def _send_email(content: str):
    logger.info("Email sent.")
