from .template_queries import OutputTemplate
from ..domain.entities import Template


def map_template_entity_to_output_dto(template: Template) -> OutputTemplate:
    return OutputTemplate(
        id=template.id,
        value=template.value,
        timestamp=template.timestamp,
    )
