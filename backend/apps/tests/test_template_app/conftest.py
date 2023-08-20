from typing import Callable

import pytest

from apps.template_app.domain.entities import Template as TemplateEntity
from .factories import TemplateEntityFactory, FakeRepository


@pytest.fixture
def template_entity() -> TemplateEntity:
    return TemplateEntityFactory()


@pytest.fixture
def fake_repository_factory() -> Callable:
    def fake_repository(initial_templates: list[TemplateEntity]) -> FakeRepository:
        return FakeRepository(templates=initial_templates)

    return fake_repository
