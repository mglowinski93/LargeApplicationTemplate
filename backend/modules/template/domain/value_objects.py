from dataclasses import dataclass

from modules.common import ids as common_ids

INITIAL_TEMPLATE_VERSION = 1


class TemplateId(common_ids.Uuid):
    pass


@dataclass(frozen=True)
class TemplateValue:
    value: int
