from typing import Callable

import pytest

from modules.common.message_bus import MessageBus
from modules.template_module.domain.commands import (
    CreateTemplate,
    DeleteTemplate,
    SetTemplateValue,
)
from modules.template_module.domain.exceptions import InvalidTemplateValue
from modules.template_module.domain.ports.exceptions import TemplateDoesNotExist
from modules.template_module.domain.value_objects import (
    INITIAL_TEMPLATE_VERSION,
    TemplateValue,
)
from modules.template_module.services import (
    create_template,
    delete_template,
    set_template_value,
)

from ..... import factories, fakers


def test_create_template_creates_template_with_none_value(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    unit_of_work = fake_template_unit_of_work_factory()

    # When
    output_template_dto = create_template(
        templates_unit_of_work=unit_of_work,
        message_bus=message_bus,
        command=CreateTemplate(),
    )

    # Then
    template = unit_of_work.templates.get(output_template_dto.id)
    assert template.value.value is None
    assert template.version == INITIAL_TEMPLATE_VERSION


def test_delete_template_deletes_template(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    template_entity = factories.TemplateEntityFactory.create()
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )

    # When
    delete_template(
        templates_unit_of_work=unit_of_work,
        command=DeleteTemplate(template_id=template_entity.id),
        message_bus=message_bus,
    )

    # Then
    assert template_entity not in unit_of_work.templates._templates


def test_delete_template_raises_exception_when_requested_template_doesnt_exist(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    with pytest.raises(TemplateDoesNotExist):
        delete_template(
            templates_unit_of_work=fake_template_unit_of_work_factory(),
            command=DeleteTemplate(template_id=fakers.fake_template_id()),
            message_bus=message_bus,
        )


def test_set_template_value_sets_value_when_valid_value(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    template_entity = factories.TemplateEntityFactory.create()
    value = fakers.fake_template_value()
    timestamp_before_setting_value = template_entity.timestamp
    version_before_setting_value = template_entity.version
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )

    # When
    set_template_value(
        templates_unit_of_work=unit_of_work,
        command=SetTemplateValue(template_id=template_entity.id, value=value),
        message_bus=message_bus,
    )

    # Then
    assert template_entity.value == value
    assert unit_of_work.templates.get(template_entity.id).value == value
    assert timestamp_before_setting_value < template_entity.timestamp
    assert version_before_setting_value + 1 == template_entity.version


def test_set_template_value_raises_exception_when_invalid_value(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    template_entity = factories.TemplateEntityFactory.create()
    value = TemplateValue(value="")
    timestamp_before_setting_value = template_entity.timestamp
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )

    # when
    with pytest.raises(InvalidTemplateValue):
        set_template_value(
            templates_unit_of_work=unit_of_work,
            command=SetTemplateValue(template_id=template_entity.id, value=value),
            message_bus=message_bus,
        )

    # Then
    assert timestamp_before_setting_value == template_entity.timestamp


def test_set_template_value_raises_exception_when_requested_template_doesnt_exist(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    value = fakers.fake_template_value()
    unit_of_work = fake_template_unit_of_work_factory()

    # When
    with pytest.raises(TemplateDoesNotExist):
        set_template_value(
            templates_unit_of_work=unit_of_work,
            command=SetTemplateValue(
                template_id=fakers.fake_template_id(), value=value
            ),
            message_bus=message_bus,
        )

    # Then
    assert not unit_of_work.templates._templates
