from __future__ import annotations

import abc
from .repository import TemplateRepository


class UnitOfWork(abc.ABC):
    templates: TemplateRepository

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        pass

    @abc.abstractmethod
    def rollback(self):
        pass
