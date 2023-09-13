from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class TemplatesFilters:
    value: Optional[str] = None
    query: Optional[str] = None
    timestamp_from: Optional[datetime] = None
    timestamp_to: Optional[datetime] = None
