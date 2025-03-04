from dataclasses import dataclass
from datetime import datetime

from ...common.domain.events import DomainEvent
from .value_objects import TemplateId, TemplateValue


@dataclass(frozen=True)
class TemplateCreated(DomainEvent):
    template_id: TemplateId
    timestamp: datetime


@dataclass(frozen=True)
class TemplateValueSet(DomainEvent):
    template_id: TemplateId
    value: TemplateValue


@dataclass(frozen=True)
class TemplateDeleted(DomainEvent):
    template_id: TemplateId
