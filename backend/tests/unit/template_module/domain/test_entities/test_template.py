import pytest

from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.entities import set_template_value
from modules.template_module.domain.exceptions import InvalidTemplateValue
from modules.template_module.domain.value_objects import TemplateId, TemplateValue

from ..... import factories, fakers


def test_set_template_value_sets_value_when_valid_value():
    # Given
    template = factories.TemplateEntityFactory.create()
    value = fakers.fake_template_value()

    # When
    template.set_value(value)

    # Then
    assert template.value == value


def test_set_template_value_raises_exception_when_invalid_value():
    template = factories.TemplateEntityFactory.create()
    timestamp_before_setting_value = template.timestamp

    with pytest.raises(InvalidTemplateValue):
        template.set_value(TemplateValue(value=""))

    assert timestamp_before_setting_value == template.timestamp


def test_set_template_value_method_value_sets_value_when_valid_value():
    # Given
    template = factories.TemplateEntityFactory.create()
    value = fakers.fake_template_value()
    timestamp_before_setting_value = template.timestamp

    # When
    set_template_value(template=template, value=value)

    # Then
    assert template.value == value
    assert timestamp_before_setting_value < template.timestamp


def test_set_template_method_raises_exception_when_invalid_value():
    template = factories.TemplateEntityFactory.create()
    timestamp_before_setting_value = template.timestamp

    with pytest.raises(InvalidTemplateValue):
        set_template_value(template=template, value=TemplateValue(value=""))

    assert timestamp_before_setting_value == template.timestamp


def test_generate_id_returns_id_of_type_template_id_type():
    # When
    template_id = TemplateEntity.generate_id()

    # Then
    assert isinstance(template_id, TemplateId)
