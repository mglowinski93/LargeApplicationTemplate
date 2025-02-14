from dataclasses import dataclass

from ..value_objects import TEMPLATE_ID_TYPE, TemplateValue
from ....common.domain.commands import Command


@dataclass(frozen=True)
class TemplateBaseCommand(Command):
    template_id: TEMPLATE_ID_TYPE


@dataclass(frozen=True)
class SetTemplateValue(TemplateBaseCommand):
    value: TemplateValue


@dataclass(frozen=True)
class CreateTemplate(TemplateBaseCommand):
    pass


@dataclass(frozen=True)
class DeleteTemplate(TemplateBaseCommand):
    pass