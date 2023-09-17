from dataclasses import dataclass

from ..value_objects import TEMPLATE_ID_TYPE, TemplateValue
from ....common.domain.events import Event


@dataclass(frozen=True)
class TemplateBaseEvent(Event):
    template_id: TEMPLATE_ID_TYPE


@dataclass(frozen=True)
class TemplateValueSet(TemplateBaseEvent):
    value: TemplateValue
