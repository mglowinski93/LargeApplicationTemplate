import pytest
from typing import Callable

from .fakers import FakeTemplateQueryRepository, FakeTemplateRepository

from modules.template_module.domain.entities import Template as TemplateEntity


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
