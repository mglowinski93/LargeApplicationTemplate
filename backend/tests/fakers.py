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


def fake_integer(min_value: int | None = None, max_value: int | None = None) -> int:
    data = {}
    if min_value is not None:
        data["min"] = min_value
    if max_value is not None:
        data["max"] = max_value

    return fake.random_int(**data)


def fake_template_value(
    min_value: int | None = None, max_value: int | None = None
) -> template_value_objects.TemplateValue:
    return template_value_objects.TemplateValue(
        value=fake_integer(min_value=min_value, max_value=max_value)
    )


class TestTaskDispatcher(common_ports.AbstractTaskDispatcher):
    @staticmethod
    def dispatch(func, *args, **kwargs):
        return func(*args, **kwargs)


class TestTemplateUnitOfWork(AbstractTemplatesUnitOfWork):
    def __init__(self, templates: list[TemplateEntity]) -> None:
        self.templates = TestTemplatesRepository(templates=templates)
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
