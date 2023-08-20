from typing import Callable

import pytest
from sqlalchemy.orm import clear_mappers, Session

from apps.template_app.domain.entities import Template as TemplateEntity
from apps.template_app.domain.value_objects import TemplateValue
from apps.template_app.adapters.repositories.sqlalchemy.orm import (
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
    def template_sqlalchemy_model(value: TemplateValue | None = None) -> TemplateEntity:
        TemplateSqlAlchemyModelFactory._meta.sqlalchemy_session = db_session
        model = TemplateSqlAlchemyModelFactory()

        if value:
            model.set_value(value)

        db_session.commit()

        return model

    return template_sqlalchemy_model
