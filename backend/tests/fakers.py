from faker import Faker

from modules.template_module.domain import value_objects as template_value_objects
from modules.common.domain import ports as common_ports

fake = Faker()


def fake_template_id() -> template_value_objects.TemplateId:
    return template_value_objects.TemplateId.new()


def fake_template_value() -> template_value_objects.TemplateValue:
    return template_value_objects.TemplateValue(value=fake.pystr(min_chars=1, max_chars=100))






class FakeTaskDispatcher(common_ports.TaskDispatcher):
    sent_emails_count = 0

    def send_email(self, content: str):  # type: ignore
        self.sent_emails_count += 1



