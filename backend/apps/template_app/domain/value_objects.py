from dataclasses import dataclass
from uuid import UUID


TEMPLATE_ID_TYPE = UUID


@dataclass(frozen=True)
class TemplateValue:
    value: str
