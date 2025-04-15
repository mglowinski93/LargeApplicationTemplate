from faker import Faker

from modules.common.domain import ports as common_ports
from modules.template.domain import value_objects as template_value_objects
from modules.template.domain.entities import Template as TemplateEntity
from modules.template.domain.ports.unit_of_work import (
    AbstractTemplatesUnitOfWork,
)
from tests.unit.template.fakers import TestTemplatesRepository

fake = Faker()


def fake_template_id() -> template_value_objects.TemplateId:
    return template_value_objects.TemplateId.new()


def fake_template_value() -> template_value_objects.TemplateValue:
    return template_value_objects.TemplateValue(value=fake.random_int(min=2, max=1000))


def fake_int(min_range: int | None = None, max_range: int | None = None) -> int:
    return fake.random_int(min=min_range, max=max_range)


def fake_negative_int() -> int:
    return fake.random_int(min=-1000, max=-1)


class TestTaskDispatcher(common_ports.AbstractTaskDispatcher):
    @staticmethod
    def dispatch(func, *args, **kwargs):
        return func(*args, **kwargs)


class TestTemplateUnitOfWork(AbstractTemplatesUnitOfWork):
    def __init__(self, templates: list[TemplateEntity]):
        self.templates = TestTemplatesRepository(templates=templates)
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
