from sqlalchemy import Table, Column, DateTime, String, UUID
from sqlalchemy.orm import composite, clear_mappers as clear_sqlalchemy_mappers

from apps.common.database import metadata, mapper_registry
from ....domain.entities import Template
from ....domain.value_objects import TemplateValue


templates = Table(
    "templates",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("value_data", String(255)),
    Column("timestamp", DateTime),
)


def start_mappers():
    # Details can be found here
    # https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#imperative-mapping
    # and
    # https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite.
    mapper_registry.map_imperatively(
        class_=Template,
        local_table=templates,
        properties={"_value": composite(TemplateValue, templates.c.value_data)},
    )


def clear_mappers():
    clear_sqlalchemy_mappers()
