from typing import Callable, Optional

import pytest

from modules.template_module.domain.entities import Template as TemplateEntity
from .fakers import (
    FakeTemplateRepository,
    FakeTemplateQueryRepository,
    FakeTemplateUnitOfWork,
    FakeMessageBus,
)
from tests.factories import FakeTaskDispatcher
from modules.template_module.adapters.repositories.sqlalchemy.consts import (
    VALUE_NAME_IN_DATABASE,
)
from modules.template_module.adapters.repositories.sqlalchemy.repository import (
    _map_template_db_to_template_entity,
)
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.value_objects import TemplateValue
from .test_adapters.test_repositories.test_sqlalchemy.factories import TemplateSqlAlchemyModelFactory
from sqlalchemy.orm import Session


@pytest.fixture
def fake_template_repository_factory() -> Callable:
    def fake_repository(
        initial_templates: list[TemplateEntity],
    ) -> FakeTemplateRepository:
        return FakeTemplateRepository(templates=initial_templates)

    return fake_repository


@pytest.fixture
def fake_template_query_repository_factory() -> Callable:
    def fake_repository(
        initial_templates: list[TemplateEntity],
    ) -> FakeTemplateQueryRepository:
        return FakeTemplateQueryRepository(templates=initial_templates)

    return fake_repository


@pytest.fixture
def fake_template_unit_of_work_factory() -> Callable:
    def fake_unit_of_work(
        initial_templates: list[TemplateEntity],
    ) -> FakeTemplateUnitOfWork:
        return FakeTemplateUnitOfWork(templates=initial_templates)

    return fake_unit_of_work


@pytest.fixture
def fake_message_bus_factory(
    fake_main_task_dispatcher_inject: FakeTaskDispatcher,
) -> Callable:
    def fake_message_bus() -> FakeMessageBus:
        return FakeMessageBus(fake_main_task_dispatcher_inject)

    return fake_message_bus


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
