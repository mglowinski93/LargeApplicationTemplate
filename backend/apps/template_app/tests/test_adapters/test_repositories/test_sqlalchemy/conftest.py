import pytest
from sqlalchemy.orm import clear_mappers, Session

from apps.template_app.adapters.repositories.sqlalchemy.database import (
    start_mappers,
    Template as TemplateSqlAlchemyModel,
)
from .factories import TemplateSqlAlchemyModelFactory


@pytest.fixture
def db_session(raw_db_session):
    start_mappers()
    yield raw_db_session
    clear_mappers()


@pytest.fixture
def template_sqlalchemy_model(db_session: Session) -> TemplateSqlAlchemyModel:
    TemplateSqlAlchemyModelFactory._meta.sqlalchemy_session = db_session
    return TemplateSqlAlchemyModelFactory()
