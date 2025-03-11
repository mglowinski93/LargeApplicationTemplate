import logging

from modules.common.domain.ports import AbstractTaskDispatcher
from modules.notifications.domain import commands as notification_domain_commands
from modules.notifications.domain.ports import AbstractEmailNotificator
from modules.notifications.services import commands as notification_commands

from ...domain.events import TemplateValueSet

logger = logging.getLogger(__name__)


def send_template_value_set_notification(
    event: TemplateValueSet,
    main_task_dispatcher: AbstractTaskDispatcher,
    email_notificator: AbstractEmailNotificator,
):
    notification_commands.send_email(
        email_notificator=email_notificator,
        task_dispatcher=main_task_dispatcher,
        command=notification_domain_commands.SendEmail(
            recipients=["admin@admin.com"],
            title="Template value set",
            content=f"Template value set for {event.template_id}.",
        ),
    )
