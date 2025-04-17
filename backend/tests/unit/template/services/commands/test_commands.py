from typing import Callable

import pytest

from modules.common.message_bus import MessageBus
from modules.template.domain.commands import (
    CreateTemplate,
    DeleteTemplate,
    SetTemplateValue,
    SubtractTemplateValue,
)
from modules.template.domain.ports.exceptions import TemplateDoesNotExist
from modules.template.domain.value_objects import (
    INITIAL_TEMPLATE_VERSION,
    TemplateValue,
)
from modules.template.services import (
    create_template,
    delete_template,
    set_template_value,
    subtract_template_value,
)

from ..... import entity_factories, fakers


def test_create_template_creates_template_with_default_value(
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
    assert template.value.value == 0
    assert template.version == INITIAL_TEMPLATE_VERSION


def test_delete_template_deletes_template(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    template_entity = entity_factories.TemplateEntityFactory.create()
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


def test_delete_template_raises_exception_when_requested_template_does_not_exist(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    with pytest.raises(TemplateDoesNotExist):
        delete_template(
            templates_unit_of_work=fake_template_unit_of_work_factory(),
            command=DeleteTemplate(template_id=fakers.fake_template_id()),
            message_bus=message_bus,
        )


def test_set_template_value_sets_value(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    template_entity = entity_factories.TemplateEntityFactory.create()
    value = fakers.fake_template_value()
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


def test_set_template_value_raises_exception_when_requested_template_does_not_exist(
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


def test_subtract_template_value_subtracts_value(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    template_entity = entity_factories.TemplateEntityFactory.create()
    template_entity.set_value(fakers.fake_template_value())
    initial_value = template_entity.value
    subtract_value = fakers.fake_template_value(max_value=initial_value.value)
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )

    # When
    subtract_template_value(
        templates_unit_of_work=unit_of_work,
        command=SubtractTemplateValue(
            template_id=template_entity.id, value=subtract_value
        ),
        message_bus=message_bus,
    )

    # Then
    assert template_entity.value == TemplateValue(
        value=initial_value.value - subtract_value.value
    )
    assert unit_of_work.templates.get(template_entity.id).value == TemplateValue(
        value=initial_value.value - subtract_value.value
    )


def test_subtract_template_value_raises_exception_when_requested_template_does_not_exist(  # noqa: E501
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    value = fakers.fake_template_value()
    unit_of_work = fake_template_unit_of_work_factory()

    # When
    with pytest.raises(TemplateDoesNotExist):
        subtract_template_value(
            templates_unit_of_work=unit_of_work,
            command=SubtractTemplateValue(
                template_id=fakers.fake_template_id(), value=value
            ),
            message_bus=message_bus,
        )

    # Then
    assert not unit_of_work.templates._templates
