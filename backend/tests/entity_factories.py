from typing import List

from modules.common import time
from modules.template.domain.entities import Template as TemplateEntity
from modules.template.domain.value_objects import (
    INITIAL_TEMPLATE_VERSION,
)

from .fakers import fake_template_id


class BatchMixin:
    @classmethod
    def create_batch(cls, size: int, **kwargs) -> List:
        if not isinstance(size, int) or size < 1:
            raise ValueError("Size must be a positive integer")

        return [cls.create(**kwargs) for _ in range(size)]  # type: ignore[attr-defined]


class TemplateEntityFactory(BatchMixin):
    @staticmethod
    def create(**kwargs) -> TemplateEntity:
        return TemplateEntity(
            id=kwargs.get("id", fake_template_id()),
            timestamp=kwargs.get("timestamp", time.get_current_timestamp()),
            version=kwargs.get("version", INITIAL_TEMPLATE_VERSION),
        )
