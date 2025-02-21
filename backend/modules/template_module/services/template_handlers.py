import inject
import logging
from typing import Callable

from ...common.domain.events import Event as DomainEvent
from ...common.domain.commands import Command as DomainCommand
from ..domain.events.template import (
    TemplateCreated,
    TemplateDeleted,
    TemplateValueSet,
)
from ..domain.commands.template import (
    CreateTemplate,
    DeleteTemplate,
    SetTemplateValue,
)
from ...common.domain.ports import TaskDispatcher
from .template_services import (
    set_template_value,
    create_template,
    delete_template,
)


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


EVENT_HANDLERS: dict[type[DomainEvent], list[Callable]] = {
    TemplateValueSet: [send_template_value_set_notification],
    TemplateCreated: [],
    TemplateDeleted: [],
}


COMMAND_HANDLERS: dict[type[DomainCommand], Callable] = {
    SetTemplateValue: set_template_value,
    CreateTemplate: create_template,
    DeleteTemplate: delete_template,
}
