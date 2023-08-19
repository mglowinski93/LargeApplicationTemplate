from sqlalchemy import Table, Column, DateTime, String, UUID, event
from sqlalchemy.orm import validates

from apps.common.database import metadata, mapper_registry
from ....domain.entities import Template, TemplateValue


templates = Table(
    "templates",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("value", String(255)),
    Column("timestamp", DateTime),
)


def parse_value_dto_to_string(value: TemplateValue) -> str:
    return f"{value.value}"


def parse_string_to_value_dto(data: str) -> TemplateValue:
    return TemplateValue(value=data)


class TemplateMapping:
    @validates("value")
    def _validate_value(self, key, value):
        """
        Transform the ValueDTO to string for database storage.
        """

        return parse_value_dto_to_string(value)

    @staticmethod
    def configure_listener():
        """
        Register an event to transform the string back to ValueDTO
        when an entity is loaded.
        """

        @event.listens_for(Template, "load")
        def receive_load(template, _):
            template.value = parse_string_to_value_dto(template.value)


def start_mappers():
    mapper_registry.map_imperatively(Template, templates)
    TemplateMapping.configure_listener()
