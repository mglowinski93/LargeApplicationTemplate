from uuid import uuid4, UUID

import factory
from faker import Faker

from apps.common.time import get_current_utc_timestamp
from apps.template_app.domain.entities import Template as TemplateEntity
from apps.template_app.domain.value_objects import TemplateValue, TEMPLATE_ID_TYPE
from apps.template_app.domain.ports import TemplateRepository, exceptions
from apps.template_app.domain.ports.unit_of_work import UnitOfWork


fake = Faker()


class TemplateEntityFactory(factory.Factory):
    class Meta:
        model = TemplateEntity

    id = factory.LazyFunction(uuid4)
    timestamp = factory.LazyFunction(get_current_utc_timestamp)


class FakeRepository(TemplateRepository):
    def __init__(self, templates: list[TemplateEntity]):
        self._templates = set(templates)

    def save(self, template: TemplateEntity):
        self._templates.add(template)

    def get(self, template_id: TEMPLATE_ID_TYPE):
        try:
            return next(
                template for template in self._templates if template.id == template_id
            )
        except StopIteration as err:
            raise exceptions.TemplateDoesNotExist(
                f"Template with id '{template_id}' doesn't exist."
            ) from err

    def list(self):
        return list(self._templates)


class FakeUnitOfWork(UnitOfWork):
    def __init__(self, templates: list[TemplateEntity]):
        self.templates = FakeRepository(templates=templates)
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def fake_template_id() -> UUID:
    return uuid4()


def fake_template_value() -> TemplateValue:
    return TemplateValue(value=fake.pystr(min_chars=1, max_chars=100))
