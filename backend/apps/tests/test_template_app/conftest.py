import pytest

from apps.template_app.domain.entities import Template as TemplateEntity
from .factories import TemplateEntityFactory


@pytest.fixture
def template_entity() -> TemplateEntity:
    return TemplateEntityFactory()
