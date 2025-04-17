import logging

from modules.notifications.domain import value_objects
from modules.notifications.domain.ports import notificators

logger = logging.getLogger(__name__)


class DummyEmailNotificator(notificators.AbstractEmailNotificator):
    total_emails_sent = 0

    @staticmethod
    def _send(data: value_objects.EmailData) -> None:
        logger.info("Sending email to %s", data.recipients)
        DummyEmailNotificator.total_emails_sent += 1
