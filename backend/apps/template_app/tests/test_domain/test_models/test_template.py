import pytest

from apps.template_app.domain.exceptions import InvalidTemplateValue
from apps.template_app.domain.models import Template, TemplateValue, set_template_value
from apps.template_app.tests.factories import fake_template_value


def test_set_template_value_sets_value_when_valid_value(template: Template):
    # Given
    value = fake_template_value()

    # When
    template.set_value(value)

    # Then
    assert template.value == value


def test_set_template_raises_exception_when_invalid_value(
    template: Template,
):
    timestamp_before_setting_value = template.timestamp

    with pytest.raises(InvalidTemplateValue):
        template.set_value(TemplateValue(value=""))

    assert timestamp_before_setting_value == template.timestamp


def test_set_template_method_value_sets_value_when_valid_value(template: Template):
    # Given
    value = fake_template_value()
    timestamp_before_setting_value = template.timestamp

    # When
    set_template_value(template=template, value=value)

    # Then
    assert template.value == value
    assert timestamp_before_setting_value < template.timestamp


def test_set_template_method_raises_exception_when_invalid_value(
    template: Template,
):
    timestamp_before_setting_value = template.timestamp

    with pytest.raises(InvalidTemplateValue):
        set_template_value(template=template, value=TemplateValue(value=""))

    assert timestamp_before_setting_value == template.timestamp
