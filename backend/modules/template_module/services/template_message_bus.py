import logging
from typing import Callable

import inject

from ..domain.events.template import TemplateValueSet
from ...common.domain.events import Event
from ...common.domain.ports import TaskDispatcher


logger = logging.getLogger(__name__)


@inject.params(task_dispatcher="main_task_dispatcher")
def send_template_value_set_notification(
    event: TemplateValueSet, task_dispatcher: TaskDispatcher
):
    logger.debug("Dispatching email about setting template value.")
    task_dispatcher.send_email(
        f"Template value set to '{event.value.value}' for template {event.template_id}."
    )
    logger.debug("Email about setting template value dispatched.")


def handle_event(event: Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


HANDLERS: dict[type[Event], list[Callable]] = {
    TemplateValueSet: [send_template_value_set_notification],
}
