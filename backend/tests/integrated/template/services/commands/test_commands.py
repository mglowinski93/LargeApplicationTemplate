from typing import Callable

import pytest

from modules.common.message_bus import MessageBus
from modules.template.domain.commands import SubtractTemplateValue
from modules.template.domain.exceptions import InvalidTemplateValue
from modules.template.domain.value_objects import TemplateValue
from modules.template.services import subtract_template_value

from ..... import entity_factories
from .....fakers import fake_int
from ....utils import TestThread


def test_concurrent_template_subtractions_are_handled(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    template_entity = entity_factories.TemplateEntityFactory.create()
    template_value = 100
    template_entity.set_value(TemplateValue(value=template_value))
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )
    first_subtraction_value = fake_int(
        min_range=template_value - 2, max_range=template_value - 1
    )

    first_thread = TestThread(
        target=subtract_template_value,
        kwargs={
            "templates_unit_of_work": unit_of_work,
            "command": SubtractTemplateValue(
                template_id=template_entity.id,
                value=TemplateValue(value=first_subtraction_value),
            ),
            "message_bus": message_bus,
        },
    )
    last_thread = TestThread(
        target=subtract_template_value,
        kwargs={
            "templates_unit_of_work": unit_of_work,
            "command": SubtractTemplateValue(
                template_id=template_entity.id,
                value=TemplateValue(
                    value=fake_int(
                        min_range=template_value - 2, max_range=template_value - 1
                    )
                ),
            ),
            "message_bus": message_bus,
        },
    )

    # When
    first_thread.start()
    last_thread.start()
    with pytest.raises(InvalidTemplateValue):
        first_thread.join()
        last_thread.join()

    # Then
    retrieved_template = unit_of_work.templates.get(template_entity.id)
    assert retrieved_template.value.value == template_value - first_subtraction_value
