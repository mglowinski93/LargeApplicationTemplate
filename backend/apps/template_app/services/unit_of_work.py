from typing import Callable

from ..domain.ports.unit_of_work import UnitOfWork
from ..adapters.repositories.sqlalchemy import SqlAlchemyTemplateRepository
from ...common.database import get_session


class SqlAlchemyTemplateUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: Callable = get_session):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.templates = SqlAlchemyTemplateRepository(self.session)
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

        self.session.close()

        return super().__exit__(exc_type, exc_value, traceback)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
