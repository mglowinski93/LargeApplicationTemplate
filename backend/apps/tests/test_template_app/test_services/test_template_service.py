import pytest

from apps.template_app.domain.exceptions import InvalidTemplateValue
from apps.template_app.domain.entities import Template as TemplateEntity
from apps.template_app.domain.value_objects import TemplateValue
from apps.template_app.services.template_service import set_template_value
from ..factories import fake_template_value


def test_set_template_value_sets_value_when_valid_value(
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


def test_set_template_raises_exception_when_invalid_value(
    template_entity: TemplateEntity,
):
    timestamp_before_setting_value = template_entity.timestamp

    with pytest.raises(InvalidTemplateValue):
        set_template_value(template=template_entity, value=TemplateValue(value=""))

    assert timestamp_before_setting_value == template_entity.timestamp
