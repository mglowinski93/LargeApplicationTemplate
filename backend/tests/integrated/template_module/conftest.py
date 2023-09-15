from typing import Callable

import pytest

from modules.template_module.domain.entities import Template as TemplateEntity
from .factories import FakeTemplateRepository, FakeTemplateUnitOfWork


@pytest.fixture
def fake_template_repository_factory() -> Callable:
    def fake_repository(
        initial_templates: list[TemplateEntity],
    ) -> FakeTemplateRepository:
        return FakeTemplateRepository(templates=initial_templates)

    return fake_repository


@pytest.fixture
def fake_template_unit_of_work_factory() -> Callable:
    def fake_unit_of_work(
        initial_templates: list[TemplateEntity],
    ) -> FakeTemplateUnitOfWork:
        return FakeTemplateUnitOfWork(templates=initial_templates)

    return fake_unit_of_work
