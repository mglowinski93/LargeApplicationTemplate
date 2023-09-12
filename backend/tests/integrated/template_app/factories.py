from typing import Optional, List

from faker import Faker

from apps.common.dtos import Ordering, OrderingEnum
from apps.common.pagination import Pagination
from apps.template_app.domain.entities import Template as TemplateEntity
from apps.template_app.domain.ports.dtos import TemplatesFilters
from apps.template_app.domain.value_objects import TEMPLATE_ID_TYPE
from apps.template_app.domain.ports import TemplateRepository, exceptions
from apps.template_app.domain.ports.unit_of_work import UnitOfWork


fake = Faker()


class FakeTemplateRepository(TemplateRepository):
    def __init__(self, templates: list[TemplateEntity]):
        self._templates = set(templates)

    def save(self, template: TemplateEntity):
        self._templates.add(template)

    def get(self, template_id: TEMPLATE_ID_TYPE) -> TemplateEntity:
        try:
            return next(
                template for template in self._templates if template.id == template_id
            )
        except StopIteration as err:
            raise exceptions.TemplateDoesNotExist(
                f"Template with id '{template_id}' doesn't exist."
            ) from err

    def list(
        self,
        filters: TemplatesFilters,
        ordering: list[Ordering],
        pagination: Optional[Pagination] = None,
    ) -> tuple[list[TemplateEntity], int]:
        templates = self._filter(templates=self._templates, filters=filters)
        templates = self._order(templates=templates, ordering=ordering)

        if pagination is not None:
            templates = self._paginate(templates=templates, pagination=pagination)

        return list(templates), len(templates)

    @staticmethod
    def _filter(
        templates: set[TemplateEntity],
        filters: TemplatesFilters,
    ) -> set[TemplateEntity]:
        if filters.value is not None:
            templates = [t for t in templates if t.value == filters.value]

        if filters.query is not None:
            templates = [
                t
                for t in templates
                if str(t.id).lower().find(filters.query.lower()) != -1
            ]

        if filters.timestamp_from is not None:
            templates = {t for t in templates if t.timestamp >= filters.timestamp_from}

        if filters.timestamp_to is not None:
            templates = {t for t in templates if t.timestamp <= filters.timestamp_to}

        return templates

    @staticmethod
    def _order(
        templates: set[TemplateEntity], ordering: List[Ordering]
    ) -> set[TemplateEntity]:
        for order in ordering:
            if order.field == "timestamp":
                sorted(
                    templates,
                    key=lambda t: t.timestamp,
                    reverse=(order.order == OrderingEnum.DESCENDING),
                )
            elif order.field == "value":
                sorted(
                    templates,
                    key=lambda t: t.value,
                    reverse=(order.order == OrderingEnum.DESCENDING),
                )

        return templates

    @staticmethod
    def _paginate(
        templates: set[TemplateEntity], pagination: Pagination
    ) -> set[TemplateEntity]:
        start = pagination.offset
        end = start + pagination.records_per_page
        return templates[start:end]


class FakeTemplateUnitOfWork(UnitOfWork):
    def __init__(self, templates: list[TemplateEntity]):
        self.templates = FakeTemplateRepository(templates=templates)
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
