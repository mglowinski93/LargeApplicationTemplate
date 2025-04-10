import pytest

from modules.template.domain.entities import Template as TemplateEntity
from modules.template.domain.exceptions import InvalidTemplateValue
from modules.template.domain.value_objects import TemplateId, TemplateValue

from ..... import entity_factories, fakers


def test_set_template_value_sets_value_when_valid_value():
    # Given
    template = entity_factories.TemplateEntityFactory.create()
    value = fakers.fake_template_value()

    # When
    template.set_value(value)

    # Then
    assert template.value == value


def test_set_template_value_raises_exception_when_invalid_value():
    template = entity_factories.TemplateEntityFactory.create()

    with pytest.raises(InvalidTemplateValue):
        template.set_value(TemplateValue(value=0))


def test_generate_id_returns_id_of_type_template_id_type():
    # When
    template_id = TemplateEntity.generate_id()

    # Then
    assert isinstance(template_id, TemplateId)
