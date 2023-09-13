from dataclasses import dataclass
from typing import Optional
from uuid import UUID


TEMPLATE_ID_TYPE = UUID


@dataclass(frozen=True)
class TemplateValue:
    value: Optional[str]
