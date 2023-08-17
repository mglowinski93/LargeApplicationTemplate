import pytest

from apps.template_app.domain.models import Template
from .factories import TemplateFactory


@pytest.fixture
def template() -> Template:
    return TemplateFactory()
