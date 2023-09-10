from uuid import uuid4, UUID

from faker import Faker

from apps.template_app.domain.entities import Template as TemplateEntity
from apps.template_app.domain.value_objects import TEMPLATE_ID_TYPE
from apps.template_app.domain.ports import TemplateRepository, exceptions
from apps.template_app.domain.ports.unit_of_work import UnitOfWork


fake = Faker()


class FakeTemplateRepository(TemplateRepository):
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


class FakeTemplateUnitOfWork(UnitOfWork):
    def __init__(self, templates: list[TemplateEntity]):
        self.templates = FakeTemplateRepository(templates=templates)
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def fake_template_id() -> UUID:
    return uuid4()
