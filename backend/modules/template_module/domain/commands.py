from dataclasses import dataclass

from ...common.domain.commands import DomainCommand
from .value_objects import TemplateId, TemplateValue


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
