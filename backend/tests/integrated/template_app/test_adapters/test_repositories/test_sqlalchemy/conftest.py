from typing import Callable, Optional

import pytest
from sqlalchemy.orm import Session

from apps.template_app.adapters.repositories.sqlalchemy.consts import (
    VALUE_NAME_IN_DATABASE,
)
from apps.template_app.adapters.repositories.sqlalchemy.repository import (
    _map_template_db_to_template_entity,
)
from apps.template_app.domain.entities import Template as TemplateEntity
from apps.template_app.domain.value_objects import TemplateValue
from .factories import TemplateSqlAlchemyModelFactory


@pytest.fixture
def db_session(raw_db_session):
    # Add here logic responsible for additional ORM configuration
    # e.g. mappers setup: https://docs.sqlalchemy.org/en/13/orm/mapping_styles.html#classical-mappings.

    yield raw_db_session


@pytest.fixture
def template_sqlalchemy_factory(db_session: Session) -> Callable:
    def template_sqlalchemy_model(
        value: Optional[TemplateValue] = None,
    ) -> TemplateEntity:
        TemplateSqlAlchemyModelFactory._meta.sqlalchemy_session = db_session
        instance = TemplateSqlAlchemyModelFactory(
            **{"value_data": {VALUE_NAME_IN_DATABASE: value.value}}
            if value is not None
            else {}
        )
        db_session.commit()

        return instance

    return template_sqlalchemy_model


@pytest.fixture
def persistent_template_entity_factory(
    template_sqlalchemy_factory: Callable,
) -> Callable:
    def template_sqlalchemy_model(
        value: Optional[TemplateValue] = None,
    ) -> TemplateEntity:
        return _map_template_db_to_template_entity(
            template_sqlalchemy_factory(value=value)
        )

    return template_sqlalchemy_model
