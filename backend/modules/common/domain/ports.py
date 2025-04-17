from abc import ABC, abstractmethod
from typing import Callable


class AbstractTaskDispatcher(ABC):
    @staticmethod
    @abstractmethod
    def dispatch(func: Callable, *args, **kwargs) -> None:
        """
        :param func: Function to dispatch.
        :param args: Positional arguments to pass to function.
        :param kwargs: Keyword arguments to pass to function
        """

        pass
