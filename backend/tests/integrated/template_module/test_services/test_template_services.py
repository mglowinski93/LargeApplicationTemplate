from typing import Callable

import pytest

from modules.template_module.domain.exceptions import InvalidTemplateValue
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.commands.template import (
    CreateTemplate,
    DeleteTemplate,
    SetTemplateValue,
)
from modules.template_module.domain.value_objects import (
    TemplateValue,
    INITIAL_TEMPLATE_VERSION,
)
from modules.template_module.domain.ports.exceptions import TemplateDoesNotExist
from modules.template_module.services import (
    create_template,
    delete_template,
    set_template_value,
)
from ...utils import TestThread
from ....factories import FakeTaskDispatcher, fake_template_id, fake_template_value


def test_create_template_creates_template_with_none_value(
    fake_template_unit_of_work_factory: Callable,
    fake_message_bus_factory: Callable,
):
    # Given
    unit_of_work = fake_template_unit_of_work_factory(initial_templates=[])
    message_bus = fake_message_bus_factory()

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
    fake_message_bus_factory: Callable,
    template_entity: TemplateEntity,
):
    # Given
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )
    message_bus = fake_message_bus_factory()

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
    fake_message_bus_factory: Callable,
):
    with pytest.raises(TemplateDoesNotExist):
        delete_template(
            templates_unit_of_work=fake_template_unit_of_work_factory(
                initial_templates=[]
            ),
            command=DeleteTemplate(template_id=fake_template_id()),
            message_bus=fake_message_bus_factory(),
        )


def test_set_template_value_sets_value_when_valid_value(
    fake_main_task_dispatcher_inject: FakeTaskDispatcher,
    fake_template_unit_of_work_factory: Callable,
    fake_message_bus_factory: Callable,
    template_entity: TemplateEntity,
):
    # Given
    value = fake_template_value()
    timestamp_before_setting_value = template_entity.timestamp
    version_before_setting_value = template_entity.version
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )
    message_bus = fake_message_bus_factory()

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
    assert fake_main_task_dispatcher_inject.sent_emails_count == 1


def test_set_template_value_raises_exception_when_invalid_value(
    fake_template_unit_of_work_factory: Callable,
    fake_message_bus_factory: Callable,
    template_entity: TemplateEntity,
):
    # Given
    value = TemplateValue(value="")
    timestamp_before_setting_value = template_entity.timestamp
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )
    message_bus = fake_message_bus_factory()

    with pytest.raises(InvalidTemplateValue):
        set_template_value(
            templates_unit_of_work=unit_of_work,
            command=SetTemplateValue(template_id=template_entity.id, value=value),
            message_bus=message_bus,
        )

    assert timestamp_before_setting_value == template_entity.timestamp


def test_set_template_value_raises_exception_when_requested_template_doesnt_exist(
    fake_template_unit_of_work_factory: Callable,
    fake_message_bus_factory: Callable,
):
    # Given
    value = fake_template_value()
    unit_of_work = fake_template_unit_of_work_factory(initial_templates=[])
    message_bus = fake_message_bus_factory()

    with pytest.raises(TemplateDoesNotExist):
        set_template_value(
            templates_unit_of_work=unit_of_work,
            command=SetTemplateValue(template_id=fake_template_id(), value=value),
            message_bus=message_bus,
        )

    assert not unit_of_work.templates._templates


def test_concurrent_template_updates_are_not_allowed(
    fake_main_task_dispatcher_inject: FakeTaskDispatcher,
    fake_template_unit_of_work_factory: Callable,
    fake_message_bus_factory: Callable,
    template_entity: TemplateEntity,
):
    # Given
    final_template_value = fake_template_value()
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )
    message_bus = fake_message_bus_factory()

    # Then
    thread1 = TestThread(
        target=set_template_value,
        kwargs={
            "templates_unit_of_work": unit_of_work,
            "command": SetTemplateValue(
                template_id=template_entity.id, value=fake_template_value()
            ),
            "message_bus": message_bus,
        },
    )
    thread2 = TestThread(
        target=set_template_value,
        kwargs={
            "templates_unit_of_work": unit_of_work,
            "command": SetTemplateValue(
                template_id=template_entity.id, value=final_template_value
            ),
            "message_bus": message_bus,
        },
    )
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    # Then
    retrieved_template = unit_of_work.templates.get(template_entity.id)
    assert retrieved_template.version == 3
    assert retrieved_template.value == final_template_value
    assert fake_main_task_dispatcher_inject.sent_emails_count == 2
