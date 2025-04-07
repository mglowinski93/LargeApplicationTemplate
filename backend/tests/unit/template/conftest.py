from typing import Callable

import pytest

from modules.template.domain.entities import Template as TemplateEntity

from .fakers import TestTemplatesQueryRepository, TestTemplatesRepository


@pytest.fixture
def fake_template_repository_factory() -> Callable:
    def fake_repository(
        initial_templates: list[TemplateEntity],
    ) -> TestTemplatesRepository:
        return TestTemplatesRepository(templates=initial_templates)

    return fake_repository


@pytest.fixture
def fake_template_query_repository_factory() -> Callable:
    def fake_repository(
        initial_templates: list[TemplateEntity] = [],
    ) -> TestTemplatesQueryRepository:
        return TestTemplatesQueryRepository(
            templates=initial_templates if initial_templates else []
        )

    return fake_repository
