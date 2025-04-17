import pytest

from modules.template.domain.entities import Template as TemplateEntity
from modules.template.domain.exceptions import InvalidTemplateValue
from modules.template.domain.value_objects import TemplateId, TemplateValue

from ..... import entity_factories, fakers


def test_set_template_value_sets_value():
    # Given
    template = entity_factories.TemplateEntityFactory.create()
    value = fakers.fake_template_value()
    version_before_set = template.version
    timestamp_before_set = template.timestamp

    # When
    template.set_value(value)

    # Then
    assert template.value == value
    assert template.version == version_before_set + 1
    assert template.timestamp == timestamp_before_set


def test_set_template_value_raises_exception_when_invalid_value():
    # Given
    template = entity_factories.TemplateEntityFactory.create()
    initial_version = template.version

    # Then
    with pytest.raises(InvalidTemplateValue):
        template.set_value(
            TemplateValue(value=fakers.fake_integer(min_value=-1000, max_value=-1))
        )
    assert template.version == initial_version


def test_subtract_template_value_subtracts_value():
    # Given
    template = entity_factories.TemplateEntityFactory.create()
    initial_value = fakers.fake_template_value()
    template._value = initial_value
    subtraction_value = TemplateValue(value=initial_value.value - 1)
    version_before_subtract = template.version
    timestamp_before_subtract = template.timestamp

    # When
    result = template.subtract_value(subtraction_value)

    # Then
    assert result.value == initial_value.value - subtraction_value.value
    assert template.version == version_before_subtract + 1
    assert template.timestamp == timestamp_before_subtract


def test_subtract_template_value_raises_exception_when_invalid():
    # Given
    template = entity_factories.TemplateEntityFactory.create()
    initial_value = fakers.fake_template_value()
    template._value = initial_value
    initial_version = template.version
    subtraction_value = TemplateValue(value=initial_value.value)

    # Then
    with pytest.raises(InvalidTemplateValue):
        template.subtract_value(subtraction_value)
    assert template.version == initial_version


def test_generate_id_returns_id_of_type_template_id_type():
    # When
    template_id = TemplateEntity.generate_id()

    # Then
    assert isinstance(template_id, TemplateId)
