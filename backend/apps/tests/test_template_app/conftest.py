from typing import Callable

import pytest

from apps.template_app.domain.entities import Template as TemplateEntity
from .factories import TemplateEntityFactory, FakeRepository, FakeUnitOfWork


@pytest.fixture
def template_entity() -> TemplateEntity:
    return TemplateEntityFactory()


@pytest.fixture
def fake_repository_factory() -> Callable:
    def fake_repository(initial_templates: list[TemplateEntity]) -> FakeRepository:
        return FakeRepository(templates=initial_templates)

    return fake_repository


@pytest.fixture
def fake_unit_of_work_factory() -> Callable:
    def fake_unit_of_work(initial_templates: list[TemplateEntity]) -> FakeUnitOfWork:
        return FakeUnitOfWork(templates=initial_templates)

    return fake_unit_of_work
