from typing import Callable

from modules.common.message_bus import MessageBus
from modules.template.domain.commands import SetTemplateValue
from modules.template.services import set_template_value

from ..... import entity_factories, fakers
from ....utils import TestThread


def test_concurrent_template_updates_are_handled(
    fake_template_unit_of_work_factory: Callable,
    message_bus: MessageBus,
):
    # Given
    template_entity = entity_factories.TemplateEntityFactory.create()
    final_template_value = fakers.fake_template_value()
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )
    threads = [
        TestThread(
            target=set_template_value,
            kwargs={
                "templates_unit_of_work": unit_of_work,
                "command": SetTemplateValue(
                    template_id=template_entity.id, value=fakers.fake_template_value()
                ),
                "message_bus": message_bus,
            },
        )
        for _ in range(100)
    ]
    last_thread = TestThread(
        target=set_template_value,
        kwargs={
            "templates_unit_of_work": unit_of_work,
            "command": SetTemplateValue(
                template_id=template_entity.id, value=final_template_value
            ),
            "message_bus": message_bus,
        },
    )
    threads.append(last_thread)

    # When
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    retrieved_template = unit_of_work.templates.get(template_entity.id)

    # Then
    assert retrieved_template.version == 102
    assert retrieved_template.value == final_template_value
