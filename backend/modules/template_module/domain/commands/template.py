from dataclasses import dataclass

from ..value_objects import TEMPLATE_ID_TYPE, TemplateValue
from ....common.domain.commands import Command


@dataclass(frozen=True)
class SetTemplateValue(Command):
    template_id: TEMPLATE_ID_TYPE
    value: TemplateValue


@dataclass(frozen=True)
class CreateTemplate(Command):
    pass


@dataclass(frozen=True)
class DeleteTemplate(Command):
    template_id: TEMPLATE_ID_TYPE
