from abc import ABC, abstractmethod


class TaskDispatcher(ABC):
    @abstractmethod
    def send_email(self, content: str) -> None:
        pass
