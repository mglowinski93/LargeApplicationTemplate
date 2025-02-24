
from typing import Callable

from ....common.domain.events import DomainEvent
from  ....common.domain.commands import DomainCommand
from .notifications import send_template_value_set_notification


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
