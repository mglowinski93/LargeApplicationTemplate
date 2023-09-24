from abc import ABC, abstractmethod


class TaskDispatcher(ABC):
    @staticmethod
    @abstractmethod
    def send_email(content: str):
        pass
