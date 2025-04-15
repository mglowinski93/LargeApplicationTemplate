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
    # Given
    template = entity_factories.TemplateEntityFactory.create()

    # Then
    with pytest.raises(InvalidTemplateValue):
        template.set_value(TemplateValue(value=fakers.fake_negative_int()))


def test_subtract_template_value_subtracts_value_when_valid():
    # Given
    template = entity_factories.TemplateEntityFactory.create()
    initial_value = fakers.fake_template_value()
    template.set_value(initial_value)
    value_to_subtract = TemplateValue(value=initial_value.value - 1)

    # When
    result = template.subtract_value(value_to_subtract)

    # Then
    assert result.value == initial_value.value - value_to_subtract.value


def test_subtract_template_value_raises_exception_when_invalid():
    # Given
    template = entity_factories.TemplateEntityFactory.create()
    initial_value = fakers.fake_template_value()
    template.set_value(initial_value)
    value_to_subtract = TemplateValue(value=initial_value.value)

    # Then
    with pytest.raises(InvalidTemplateValue):
        template.subtract_value(value_to_subtract)


def test_generate_id_returns_id_of_type_template_id_type():
    # When
    template_id = TemplateEntity.generate_id()

    # Then
    assert isinstance(template_id, TemplateId)
