from typing import Optional

from .dtos import OutputTemplate, DetailedOutputTemplate
from .mappers import (
    map_template_entity_to_output_dto,
    map_template_entity_to_output_detailed_dto,
)
from .ports import AbstractTemplatesQueryRepository
from ...domain.ports.dtos import TemplatesFilters
from ...domain.value_objects import TemplateId
from ....common.dtos import Ordering, OrderingEnum
from ....common.pagination import Pagination


def get_template(
    templates_query_repository: AbstractTemplatesQueryRepository,
    template_id: TemplateId,
) -> DetailedOutputTemplate:
    return map_template_entity_to_output_detailed_dto(
        templates_query_repository.get(template_id)
    )


def list_templates(
    templates_query_repository: AbstractTemplatesQueryRepository,
    filters: Optional[TemplatesFilters] = None,
    ordering: Optional[list[Ordering]] = None,
    pagination: Optional[Pagination] = None,
) -> tuple[list[OutputTemplate], int]:
    if filters is None:
        filters = TemplatesFilters()

    if ordering is None:
        ordering = [Ordering(field="timestamp", order=OrderingEnum.DESCENDING)]

    templates, all_templates_count = templates_query_repository.list(
        filters=filters,
        ordering=ordering,
        pagination=pagination,
    )
    return [
        map_template_entity_to_output_dto(template) for template in templates
    ], all_templates_count
