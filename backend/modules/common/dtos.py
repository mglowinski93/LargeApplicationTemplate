from dataclasses import dataclass
from enum import Enum


class OrderingEnum(Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


@dataclass(frozen=True)
class Ordering:
    field: str
    order: OrderingEnum
