from typing import Callable, Optional

import pytest
from sqlalchemy.orm import Session

from modules.template_module.adapters.repositories.sqlalchemy.consts import (
    VALUE_NAME_IN_DATABASE,
)
from modules.template_module.adapters.repositories.sqlalchemy.repository import (
    _map_template_db_to_template_entity,
)
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.value_objects import TemplateValue
from .factories import TemplateSqlAlchemyModelFactory


@pytest.fixture
def template_sqlalchemy_factory(db_session: Session) -> Callable:
    def template_sqlalchemy_model(
        value: Optional[TemplateValue] = None,
    ) -> TemplateEntity:
        db_session
        TemplateSqlAlchemyModelFactory._meta.sqlalchemy_session = (  # type: ignore
            db_session
        )
        instance = TemplateSqlAlchemyModelFactory.create(
            **{"value_data": {VALUE_NAME_IN_DATABASE: value.value}}
            if value is not None
            else {}
        )
        db_session.commit()

        return instance  # type: ignore

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
