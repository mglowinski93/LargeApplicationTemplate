from typing import Callable

import pytest
from sqlalchemy.orm import clear_mappers, Session

from apps.template_app.adapters.repositories.sqlalchemy.database import (
    start_mappers,
)
from .factories import TemplateSqlAlchemyModelFactory


@pytest.fixture
def db_session(raw_db_session):
    start_mappers()
    yield raw_db_session
    clear_mappers()


@pytest.fixture
def template_sqlalchemy_factory(db_session: Session) -> Callable:
    def template_sqlalchemy_model():
        TemplateSqlAlchemyModelFactory._meta.sqlalchemy_session = db_session
        model = TemplateSqlAlchemyModelFactory()
        db_session.commit()
        return model

    return template_sqlalchemy_model
