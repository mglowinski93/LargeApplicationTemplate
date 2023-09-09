import pytest

from apps.template_app.domain.exceptions import InvalidTemplateValue
from apps.template_app.domain.entities import (
    Template as TemplateEntity,
    set_template_value,
)
from apps.template_app.domain.value_objects import TemplateValue, TEMPLATE_ID_TYPE
from ...factories import fake_template_value


def test_set_template_value_sets_value_when_valid_value(
    template_entity: TemplateEntity,
):
    # Given
    value = fake_template_value()

    # When
    template_entity.set_value(value)

    # Then
    assert template_entity.value == value


def test_set_template_value_raises_exception_when_invalid_value(
    template_entity: TemplateEntity,
):
    timestamp_before_setting_value = template_entity.timestamp

    with pytest.raises(InvalidTemplateValue):
        template_entity.set_value(TemplateValue(value=""))

    assert timestamp_before_setting_value == template_entity.timestamp


def test_set_template_value_method_value_sets_value_when_valid_value(
    template_entity: TemplateEntity,
):
    # Given
    value = fake_template_value()
    timestamp_before_setting_value = template_entity.timestamp

    # When
    set_template_value(template=template_entity, value=value)

    # Then
    assert template_entity.value == value
    assert timestamp_before_setting_value < template_entity.timestamp


def test_set_template_method_raises_exception_when_invalid_value(
    template_entity: TemplateEntity,
):
    timestamp_before_setting_value = template_entity.timestamp

    with pytest.raises(InvalidTemplateValue):
        set_template_value(template=template_entity, value=TemplateValue(value=""))

    assert timestamp_before_setting_value == template_entity.timestamp


def test_generate_id_returns_id_of_type_template_id_type():
    # When
    template_id = TemplateEntity.generate_id()

    # Then
    assert isinstance(template_id, TEMPLATE_ID_TYPE)
