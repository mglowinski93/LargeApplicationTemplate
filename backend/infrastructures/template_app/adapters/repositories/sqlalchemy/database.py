from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime
from sqlalchemy.orm import mapper

from apps.template_app.domain.models import Template


metadata = MetaData()


templates = Table(
    "templates",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("value", String(255)),
    Column("timestamp", DateTime),
)


def start_mappers():
    mapper(Template, templates)
