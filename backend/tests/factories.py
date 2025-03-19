from typing import Generic, List, TypeVar

import factory

from modules.common import time
from modules.template_module.adapters.repositories.sqlalchemy.consts import (
    VALUE_NAME_IN_DATABASE,
)
from modules.template_module.adapters.repositories.sqlalchemy.orm import (
    Template as SqlAlchemyTemplateDb,
)
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.value_objects import (
    INITIAL_TEMPLATE_VERSION,
)

from .fakers import fake_template_id, fake_template_value

T = TypeVar("T")


class BatchMixin(Generic[T]):
    @classmethod
    def create_batch(cls, size: int, **kwargs) -> List[T]:
        if not isinstance(size, int) or size < 1:
            raise ValueError("Size must be a positive integer")

        return [cls.create(**kwargs) for _ in range(size)]  # type: ignore[attr-defined]


class TemplatePersistentEntityFactory(
    factory.alchemy.SQLAlchemyModelFactory,
):
    class Meta:
        model = SqlAlchemyTemplateDb
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(fake_template_id)
    value_data = factory.LazyFunction(
        lambda: {VALUE_NAME_IN_DATABASE: fake_template_value().value}
    )
    timestamp = factory.LazyFunction(time.get_current_timestamp)
    version = INITIAL_TEMPLATE_VERSION


class TemplateEntityFactory(BatchMixin[TemplateEntity]):
    @staticmethod
    def create(**kwargs) -> TemplateEntity:
        return TemplateEntity(
            id=kwargs.get("id", fake_template_id()),
            timestamp=kwargs.get("timestamp", time.get_current_timestamp()),
            version=kwargs.get("version", INITIAL_TEMPLATE_VERSION),
        )
