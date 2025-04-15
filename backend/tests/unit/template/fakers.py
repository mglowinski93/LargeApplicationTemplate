from typing import List

from modules.common.dtos import Ordering, OrderingEnum
from modules.common.pagination import Pagination
from modules.template.domain.entities import Template as TemplateEntity
from modules.template.domain.ports import (
    AbstractTemplatesDomainRepository,
    exceptions,
)
from modules.template.domain.ports.dtos import TemplatesFilters
from modules.template.domain.value_objects import TemplateId
from modules.template.services.queries.ports import (
    AbstractTemplatesQueryRepository,
)


class TestTemplatesRepository(AbstractTemplatesDomainRepository):
    def __init__(self, templates: list[TemplateEntity]):
        self._templates = set(templates)

    def create(self, template: TemplateEntity):
        # Template entities can be compared, due ot that hash method is implemented.
        if template in self._templates:
            self._templates.remove(template)
        self._templates.add(template)

    def delete(self, template_id: TemplateId):
        self._templates.remove(self.get(template_id=template_id))

    def get(self, template_id: TemplateId) -> TemplateEntity:
        try:
            return next(
                template for template in self._templates if template.id == template_id
            )
        except StopIteration as err:
            raise exceptions.TemplateDoesNotExist(
                f"Template with id '{template_id}' doesn't exist."
            ) from err

    def update(self, template: TemplateEntity):
        self._templates.remove(self.get(template_id=template.id))
        self._templates.add(template)


class TestTemplatesQueryRepository(AbstractTemplatesQueryRepository):
    def __init__(self, templates: list[TemplateEntity]):
        self._templates = set(templates)

    def get(self, template_id: TemplateId) -> TemplateEntity:
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
        ordering: list[Ordering | None],
        pagination: Pagination | None = None,
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
        if filters.query is not None:
            templates = {
                template
                for template in templates
                if str(template.id).lower().find(filters.query.lower()) != -1
            }

        if filters.timestamp_from is not None:
            templates = {
                template
                for template in templates
                if template.timestamp >= filters.timestamp_from
            }

        if filters.timestamp_to is not None:
            templates = {
                template
                for template in templates
                if template.timestamp <= filters.timestamp_to
            }

        return templates

    @staticmethod
    def _order(
        templates: set[TemplateEntity], ordering: List[Ordering | None]
    ) -> set[TemplateEntity]:
        for order in ordering:
            if order is None:
                continue
            if order.field == "timestamp":
                sorted(
                    templates,
                    key=lambda template: (template.value is None, template.value),
                    reverse=(order.order == OrderingEnum.DESCENDING),
                )
            elif order.field == "value":
                sorted(
                    templates,
                    key=lambda template: (template.value is None, template.value),
                    reverse=(order.order == OrderingEnum.DESCENDING),
                )

        return templates

    @staticmethod
    def _paginate(
        templates: set[TemplateEntity], pagination: Pagination
    ) -> set[TemplateEntity]:
        start = pagination.offset
        return set(list(templates)[start : start + pagination.records_per_page])
