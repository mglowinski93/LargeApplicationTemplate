from modules.common.dtos import Ordering, OrderingEnum
from modules.common.pagination import Pagination

from ...domain.ports.dtos import TemplatesFilters
from ...domain.value_objects import TemplateId
from .dtos import DetailedOutputTemplate, OutputTemplate
from .mappers import (
    map_template_entity_to_output_detailed_dto,
    map_template_entity_to_output_dto,
)
from .ports import AbstractTemplatesQueryRepository


def get_template(
    templates_query_repository: AbstractTemplatesQueryRepository,
    template_id: TemplateId,
) -> DetailedOutputTemplate:
    return map_template_entity_to_output_detailed_dto(
        templates_query_repository.get(template_id)
    )


def list_templates(
    templates_query_repository: AbstractTemplatesQueryRepository,
    filters: TemplatesFilters | None = None,
    ordering: list[Ordering] | None = None,
    pagination: Pagination | None = None,
) -> tuple[list[OutputTemplate], int]:
    if filters is None:
        filters = TemplatesFilters()

    if ordering is None:
        ordering = [Ordering(field="timestamp", order=OrderingEnum.DESCENDING)]

    templates, count = templates_query_repository.list(
        filters=filters,
        ordering=ordering,
        pagination=pagination,
    )
    return [
        map_template_entity_to_output_dto(template) for template in templates
    ], count
