from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ...domain.value_objects import TemplateId, TemplateValue


@dataclass
class OutputTemplate:
    id: TemplateId
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
