import logging

from ....common.domain.ports import TaskDispatcher
from ...domain.events import TemplateValueSet

logger = logging.getLogger(__name__)


def send_template_value_set_notification(
    event: TemplateValueSet, main_task_dispatcher: TaskDispatcher
):
    logger.info("Dispatching email about setting template value.")
    main_task_dispatcher.send_email(
        f"Template value set to '{event.value.value}' for template {event.template_id}."
    )
    logger.info("Email about setting template value dispatched.")
