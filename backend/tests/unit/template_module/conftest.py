import pytest
from typing import Callable

from .fakers import FakeTemplatesQueryRepository, FakeTemplatesRepository

from modules.template_module.domain.entities import Template as TemplateEntity


@pytest.fixture
def fake_template_repository_factory() -> Callable:
    def fake_repository(
        initial_templates: list[TemplateEntity],
    ) -> FakeTemplatesRepository:
        return FakeTemplatesRepository(templates=initial_templates)

    return fake_repository


@pytest.fixture
def fake_template_query_repository_factory() -> Callable:
    def fake_repository(
        initial_templates: list[TemplateEntity] = [],
    ) -> FakeTemplatesQueryRepository:
        return FakeTemplatesQueryRepository(
            templates=initial_templates if initial_templates else []
        )

    return fake_repository
