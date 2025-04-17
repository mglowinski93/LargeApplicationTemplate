from typing import Callable

import pytest

from modules.common.message_bus import MessageBus
from modules.template.domain.commands import SubtractTemplateValue
from modules.template.domain.exceptions import InvalidTemplateValue
from modules.template.domain.value_objects import TemplateValue
from modules.template.services import subtract_template_value

from ..... import entity_factories
from .....fakers import fake_template_value
from ....utils import TestThread


def test_concurrent_template_subtractions_are_handled(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    template_entity = entity_factories.TemplateEntityFactory.create()
    template_entity.set_value(fake_template_value(min_value=3))
    initial_value = template_entity.value
    initial_version = template_entity.version
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )
    subtraction_value = fake_template_value(
        min_value=template_entity.value.value - 2,
        max_value=template_entity.value.value - 1,
    )

    thread_1 = TestThread(
        target=subtract_template_value,
        kwargs={
            "templates_unit_of_work": unit_of_work,
            "command": SubtractTemplateValue(
                template_id=template_entity.id,
                value=subtraction_value,
            ),
            "message_bus": message_bus,
        },
    )
    thread_2 = TestThread(
        target=subtract_template_value,
        kwargs={
            "templates_unit_of_work": unit_of_work,
            "command": SubtractTemplateValue(
                template_id=template_entity.id,
                value=subtraction_value,
            ),
            "message_bus": message_bus,
        },
    )

    # When
    thread_1.start()
    thread_2.start()
    with pytest.raises(InvalidTemplateValue):
        thread_1.join()
        thread_2.join()

    # Then
    assert template_entity.value == TemplateValue(
        initial_value.value - subtraction_value.value
    )
    assert template_entity.version == initial_version + 1

    retrieved_template = unit_of_work.templates.get(template_entity.id)
    assert retrieved_template.value == TemplateValue(
        initial_value.value - subtraction_value.value
    )
    assert retrieved_template.version == initial_version + 1
