import logging
from typing import Callable

from ..domain.events.template import TemplateValueSet
from ...common.domain.events import Event

logger = logging.getLogger(__name__)


def handle_event(event: Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_template_value_set_notification(event: TemplateValueSet):
    logger.info(
        f"Template value set to '{event.value.value}' for template {event.template_id}."
    )


HANDLERS: dict[type[Event], list[Callable]] = {
    TemplateValueSet: [send_template_value_set_notification],
}
