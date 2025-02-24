from typing import Optional

from .dtos import OutputTemplate, DetailedOutputTemplate
from .mappers import (
    map_template_entity_to_output_dto,
    map_template_entity_to_output_detailed_dto,
)
from ..domain.ports.dtos import TemplatesFilters
from ..domain.value_objects import TEMPLATE_ID_TYPE
from ...common.dtos import Ordering, OrderingEnum
from ...common.pagination import Pagination
from ...template_module.adapters.repositories.sqlalchemy import (
    SqlAlchemyTemplateQueryRepository,
)


def get_template(
    query_repository: SqlAlchemyTemplateQueryRepository,
    template_id: TEMPLATE_ID_TYPE,
) -> DetailedOutputTemplate:
    return map_template_entity_to_output_detailed_dto(query_repository.get(template_id))


def list_templates(
    query_repository: SqlAlchemyTemplateQueryRepository,
    filters: Optional[TemplatesFilters] = None,
    ordering: Optional[list[Ordering]] = None,
    pagination: Optional[Pagination] = None,
) -> tuple[list[OutputTemplate], int]:
    if filters is None:
        filters = TemplatesFilters()

    if ordering is None:
        ordering = [Ordering(field="timestamp", order=OrderingEnum.DESCENDING)]

    templates, all_templates_count = query_repository.list(
        filters=filters,
        ordering=ordering,
        pagination=pagination,
    )
    return [
        map_template_entity_to_output_dto(template) for template in templates
    ], all_templates_count
