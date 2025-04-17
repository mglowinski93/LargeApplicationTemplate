from dataclasses import dataclass
from datetime import datetime

from ...domain.value_objects import TemplateId, TemplateValue


@dataclass
class OutputTemplate:
    id: TemplateId
    timestamp: datetime

    def serialize(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
        }


@dataclass
class DetailedOutputTemplate(OutputTemplate):
    value: TemplateValue

    def serialize(self):
        return {
            "id": self.id,
            "value": self.value.value,
            "timestamp": self.timestamp,
        }
