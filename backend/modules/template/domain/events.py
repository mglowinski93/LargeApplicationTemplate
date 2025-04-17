from dataclasses import dataclass
from datetime import datetime

from modules.common.domain.events import DomainEvent

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
class TemplateValueSubtracted(DomainEvent):
    template_id: TemplateId
    subtracted_value: TemplateValue
    final_value: TemplateValue


@dataclass(frozen=True)
class TemplateDeleted(DomainEvent):
    template_id: TemplateId
