from faker import Faker

from modules.common.domain import ports as common_ports
from modules.template_module.domain import value_objects as template_value_objects
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.ports.unit_of_work import (
    AbstractTemplatesUnitOfWork,
)
from tests.unit.template_module.fakers import TestTemplatesRepository

fake = Faker()


def fake_template_id() -> template_value_objects.TemplateId:
    return template_value_objects.TemplateId.new()


def fake_template_value() -> template_value_objects.TemplateValue:
    return template_value_objects.TemplateValue(
        value=fake.pystr(min_chars=1, max_chars=100)
    )


class TestTaskDispatcher(common_ports.TaskDispatcher):
    sent_emails_count = 0

    def send_email(self, content: str):  # type: ignore
        self.sent_emails_count += 1


class TestTemplateUnitOfWork(AbstractTemplatesUnitOfWork):
    def __init__(self, templates: list[TemplateEntity]):
        self.templates = TestTemplatesRepository(templates=templates)
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
