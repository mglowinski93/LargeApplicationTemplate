from collections import deque
from typing import Sequence
from faker import Faker

from modules.template_module.domain.ports.unit_of_work import (
    AbstractTemplatesUnitOfWork,
)
from tests.unit.template_module.fakers import FakeTemplateRepository
from modules.template_module.domain import value_objects as template_value_objects
from modules.template_module.domain.events import TemplateValueSet
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.common.domain import ports as common_ports
from modules.common.domain import events, commands
from modules.common.message_bus import Message, MessageBus


fake = Faker()


def fake_template_id() -> template_value_objects.TemplateId:
    return template_value_objects.TemplateId.new()


def fake_template_value() -> template_value_objects.TemplateValue:
    return template_value_objects.TemplateValue(
        value=fake.pystr(min_chars=1, max_chars=100)
    )


class FakeTaskDispatcher(common_ports.TaskDispatcher):
    sent_emails_count = 0

    def send_email(self, content: str):  # type: ignore
        self.sent_emails_count += 1


class FakeTemplateUnitOfWork(AbstractTemplatesUnitOfWork):
    def __init__(self, templates: list[TemplateEntity]):
        self.templates = FakeTemplateRepository(templates=templates)
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakeMessageBus(MessageBus):
    def __init__(self, fake_task_dispatcher: FakeTaskDispatcher):
        self.queue: deque[Message] = deque()
        self.fake_task_dispatcher = fake_task_dispatcher

    def handle(self, messages: Sequence[Message]):
        self.queue.extend(messages)

        while self.queue:
            message = self.queue.popleft()

            if isinstance(message, events.DomainEvent):
                self.handle_event(message)
            elif isinstance(message, commands.DomainCommand):
                self.handle_command(message)

    def handle_event(self, event: events.DomainEvent):
        if isinstance(event, TemplateValueSet):
            self.fake_task_dispatcher.send_email("test")
        else:
            pass

    def handle_command(self, command: commands.DomainCommand):
        pass