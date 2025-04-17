from typing import Callable

from ....common.domain.commands import DomainCommand
from ....common.domain.events import DomainEvent
from ...domain.commands import (
    CreateTemplate,
    DeleteTemplate,
    SetTemplateValue,
    SubtractTemplateValue,
)
from ...domain.events import (
    TemplateCreated,
    TemplateDeleted,
    TemplateValueSet,
    TemplateValueSubtracted,
)
from ...services.commands import (
    create_template,
    delete_template,
    set_template_value,
    subtract_template_value,
)
from .notifications import send_template_value_set_notification

EVENT_HANDLERS: dict[type[DomainEvent], list[Callable]] = {
    TemplateValueSet: [send_template_value_set_notification],
    TemplateValueSubtracted: [],
    TemplateCreated: [],
    TemplateDeleted: [],
}


COMMAND_HANDLERS: dict[type[DomainCommand], Callable] = {
    SetTemplateValue: set_template_value,
    SubtractTemplateValue: subtract_template_value,
    CreateTemplate: create_template,
    DeleteTemplate: delete_template,
}
