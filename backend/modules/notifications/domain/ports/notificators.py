from abc import ABC, abstractmethod

from ....common.domain import ports as common_ports
from ..value_objects import EmailData


class AbstractEmailNotificator(ABC):
    @staticmethod
    @abstractmethod
    def _send(data: EmailData) -> None:
        pass

    @classmethod
    def send(
        cls,
        task_dispatcher: common_ports.AbstractTaskDispatcher,
        data: EmailData,
    ) -> None:
        """
        :param task_dispatcher: Task dispatcher to queue the task.
        :param data: Data to send in email.
        :raises FailedToSendEmail: E-mail was not sent.
        """
        task_dispatcher.dispatch(func=cls._send, data=data)
