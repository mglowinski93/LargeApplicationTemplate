from modules.common.domain import ports as common_ports

from ..domain import commands, ports, value_objects


def send_email(
    email_notificator: ports.AbstractEmailNotificator,
    task_dispatcher: common_ports.AbstractTaskDispatcher,
    command: commands.SendEmail,
) -> None:
    email_notificator.send(
        task_dispatcher=task_dispatcher,
        data=value_objects.EmailData(
            recipients=command.recipients,
            title=command.title,
            content=command.content,
        ),
    )
