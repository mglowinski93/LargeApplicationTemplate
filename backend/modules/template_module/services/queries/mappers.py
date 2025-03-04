from ...domain.entities import Template
from .dtos import DetailedOutputTemplate, OutputTemplate


def map_template_entity_to_output_dto(template: Template) -> OutputTemplate:
    return OutputTemplate(
        id=template.id,
        timestamp=template.timestamp,
    )


def map_template_entity_to_output_detailed_dto(
    template: Template,
) -> DetailedOutputTemplate:
    return DetailedOutputTemplate(
        id=template.id,
        value=template.value,
        timestamp=template.timestamp,
    )
