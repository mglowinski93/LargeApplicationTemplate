from dataclasses import dataclass

from .value_objects import TemplateId, TemplateValue
from ...common.domain.commands import DomainCommand


@dataclass(frozen=True)
class SetTemplateValue(DomainCommand):
    template_id: TemplateId
    value: TemplateValue


@dataclass(frozen=True)
class CreateTemplate(DomainCommand):
    pass


@dataclass(frozen=True)
class DeleteTemplate(DomainCommand):
    template_id: TemplateId
