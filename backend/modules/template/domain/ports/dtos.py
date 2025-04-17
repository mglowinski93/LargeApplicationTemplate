from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TemplatesFilters:
    value: int | None = None
    query: str | None = None
    timestamp_from: datetime | None = None
    timestamp_to: datetime | None = None
