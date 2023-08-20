from sqlalchemy import Table, Column, DateTime, String, UUID

from apps.common.database import metadata, mapper_registry
from ....domain.entities import Template


templates = Table(
    "templates",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("value", String(255)),
    Column("timestamp", DateTime),
)


def start_mappers():
    # Details can be found here
    # https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#imperative-mapping
    # and
    # https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite.
    mapper_registry.map_imperatively(Template, templates)
