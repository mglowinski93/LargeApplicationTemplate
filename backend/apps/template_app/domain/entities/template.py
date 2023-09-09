from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import uuid4

from ..exceptions import InvalidTemplateValue
from ...domain.value_objects import TEMPLATE_ID_TYPE, TemplateValue
from ....common.time import get_current_utc_timestamp


def set_template_value(template: Template, value: TemplateValue):
    """
    This is optional method only needed when
    there is a logic related to particular action,
    that can't be placed in entity,
    due to it's not related to business logic, or it's too complicated.
    """

    template.set_value(value)
    template.timestamp = get_current_utc_timestamp()


class Template:
    """
    Allocate here business logic and high-level rules that are related to this entity.
    """

    def __init__(self, id: TEMPLATE_ID_TYPE, timestamp: datetime):
        self.id = id
        self._value: Optional[TemplateValue] = None
        self.timestamp = timestamp

    @property
    def value(self) -> Optional[TemplateValue]:
        return self._value

    @staticmethod
    def generate_id() -> TEMPLATE_ID_TYPE:
        return uuid4()

    def set_value(self, value: TemplateValue):
        if isinstance(value.value, str) and len(value.value):
            self._value = value
            return

        raise InvalidTemplateValue(f"Invalid value: '{value.value}'")

    def __repr__(self):
        return f"Template {self.id}"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Template) and vars(self) == vars(other)

    def __hash__(self):
        return hash(self.id)
