from typing import Optional

from .dtos import OutputTemplate
from .mappers import map_template_entity_to_output_dto
from ..domain.ports.dtos import TemplatesFilters
from ..domain.value_objects import TEMPLATE_ID_TYPE
from ..domain.ports.unit_of_work import AbstractTemplatesUnitOfWork
from ...common.dtos import Ordering, OrderingEnum
from ...common.pagination import Pagination


# In case of low efficiency,
# this can be refactored to use the CQRS pattern.
# More details can be found here:
# https://www.cosmicpython.com/book/chapter_12_cqrs.html.


def get_template(
    unit_of_work: AbstractTemplatesUnitOfWork,
    template_id: TEMPLATE_ID_TYPE,
) -> OutputTemplate:
    with unit_of_work:
        return map_template_entity_to_output_dto(
            unit_of_work.templates.get(template_id)
        )


def list_templates(
    unit_of_work: AbstractTemplatesUnitOfWork,
    filters: Optional[TemplatesFilters] = None,
    ordering: Optional[list[Ordering]] = None,
    pagination: Optional[Pagination] = None,
) -> tuple[list[OutputTemplate], int]:
    if filters is None:
        filters = TemplatesFilters()

    if ordering is None:
        ordering = [Ordering(field="timestamp", order=OrderingEnum.DESCENDING)]

    with unit_of_work:
        templates, all_templates_count = unit_of_work.templates.list(
            filters=filters,
            ordering=ordering,
            pagination=pagination,
        )
        return [
            map_template_entity_to_output_dto(template) for template in templates
        ], all_templates_count
