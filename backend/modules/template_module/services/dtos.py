from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..domain.value_objects import TEMPLATE_ID_TYPE, TemplateValue


@dataclass
class OutputTemplate:
    id: TEMPLATE_ID_TYPE
    value: Optional[TemplateValue]
    timestamp: datetime

    def serialize(self):
        return {
            "id": self.id,
            "value": self.value.value,
            "timestamp": self.timestamp,
        }


@dataclass
class DetailedOutputTemplate(OutputTemplate):
    pass
