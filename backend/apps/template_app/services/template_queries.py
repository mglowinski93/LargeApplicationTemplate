from .dto import OutputTemplate
from .mappers import map_template_entity_to_output_dto
from ..domain.value_objects import TEMPLATE_ID_TYPE
from ..domain.ports.unit_of_work import UnitOfWork


def get_template(
    unit_of_work: UnitOfWork,
    template_id: TEMPLATE_ID_TYPE,
) -> OutputTemplate:
    with unit_of_work:
        return map_template_entity_to_output_dto(
            unit_of_work.templates.get(template_id)
        )


def list_templates(unit_of_work: UnitOfWork) -> list[OutputTemplate]:
    with unit_of_work:
        return [
            map_template_entity_to_output_dto(template)
            for template in unit_of_work.templates.list()
        ]
