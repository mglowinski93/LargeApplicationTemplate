from __future__ import annotations

from datetime import datetime

from modules.common.domain.events import DomainEvent

from ...domain.value_objects import TemplateId, TemplateValue
from ..exceptions import InvalidTemplateValue


class Template:
    """
    Allocate here business logic and high-level rules that are related to this entity.
    """

    def __init__(self, id: TemplateId, timestamp: datetime, version: int) -> None:
        self.id = id
        self._value: TemplateValue = TemplateValue(value=0)
        self.timestamp = timestamp
        self.version = version
        self.messages: list[DomainEvent] = []

    @property
    def value(self) -> TemplateValue:
        return self._value

    @staticmethod
    def generate_id() -> TemplateId:
        return TemplateId.new()

    def set_value(self, value: TemplateValue) -> None:
        if value.value <= 0:
            raise InvalidTemplateValue(
                f"Invalid value: '{value.value}', must be above 0."
            )

        self._value = value
        self.version += 1

    def subtract_value(self, value: TemplateValue) -> TemplateValue:
        result = self._value.value - value.value

        if result <= 0:
            raise InvalidTemplateValue(f"Invalid value: '{result}', must be above 0.")

        self._value = TemplateValue(value=result)
        self.version += 1
        return TemplateValue(value=result)

    def __repr__(self):
        return f"Template {self.id}"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Template) and vars(self) == vars(other)

    def __hash__(self):
        return hash(self.id)
