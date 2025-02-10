from typing import Callable, Optional

from sqlalchemy.orm import Session

from ..domain.ports.unit_of_work import AbstractTemplatesUnitOfWork
from ..adapters.repositories.sqlalchemy import SqlAlchemyTemplateDomainRepository
from ...common.database import get_session


class SqlAlchemyTemplatesUnitOfWork(AbstractTemplatesUnitOfWork):
    def __init__(self, session_factory: Callable = get_session):
        self.session_factory: Callable = session_factory
        self._session: Optional[Session] = None

    def __enter__(self):
        self._session = self.session_factory()
        self.templates = SqlAlchemyTemplateDomainRepository(self._session)
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

        self._session.close()

        return super().__exit__(exc_type, exc_value, traceback)

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError("Database session not initialized.")

        return self._session

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
