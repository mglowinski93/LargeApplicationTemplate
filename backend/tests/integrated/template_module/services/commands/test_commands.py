from typing import Callable

import pytest

from modules.common.message_bus import MessageBus
from modules.template_module.domain.commands import (
    CreateTemplate,
    DeleteTemplate,
    SetTemplateValue,
)
from modules.template_module.services import (
    create_template,
    delete_template,
    set_template_value,
)
from ....utils import TestThread
from .....unit import factories
from ..... import fakers


def test_concurrent_template_updates_are_handled(
    fake_main_task_dispatcher_inject: fakers.FakeTaskDispatcher,
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    template_entity = factories.TemplateEntityFactory.create()
    final_template_value = fakers.fake_template_value()
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )

    # Then
    thread1 = TestThread(
        target=set_template_value,
        kwargs={
            "templates_unit_of_work": unit_of_work,
            "command": SetTemplateValue(
                template_id=template_entity.id, value=fakers.fake_template_value()
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
