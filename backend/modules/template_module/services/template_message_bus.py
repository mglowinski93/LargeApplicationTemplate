import logging
from typing import Callable

import inject

from ..domain.events.template import (
    TemplateValueSet,
    TemplateCreated,
    TemplateDeleted,
)
from ..domain.commands.template import (
    SetTemplateValue,
    CreateTemplate,
    DeleteTemplate,
)
from ...common.domain.events import Event
from ...common.domain.commands import Command
from ...common.domain.ports import TaskDispatcher
from .template_services import (
    set_template_value,
    create_template,
    delete_template,
)


logger = logging.getLogger(__name__)
Message = Event | Command


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
    for handler in EVENT_HANDLERS[type(event)]:
        handler(event)


def handle_command(command: Command):
    try:
        handler = COMMAND_HANDLERS[type(command)]
        result = handler(command)
        return result
    except Exception as exception:
        logger.exception("Exception handling command %s", command)
        raise exception


def handle(
    message: Message
):
    if isinstance(message, Event):
        handle_event(message)
    elif isinstance(message, Command):
        handle_command(message)
    else:
        raise Exception(f"{message} was not an Event or Command.")


EVENT_HANDLERS: dict[type[Event], list[Callable]] = {
    TemplateValueSet: [send_template_value_set_notification],
    TemplateCreated: [],
    TemplateDeleted: [],
}


COMMAND_HANDLERS: dict[type[Command], list[Callable]] = {
    SetTemplateValue: [set_template_value],
    CreateTemplate: [create_template],
    DeleteTemplate: [delete_template],
}
