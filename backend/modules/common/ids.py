import uuid
from typing import Self


class Uuid(uuid.UUID):
    @classmethod
    def new(cls) -> Self:
        return cls(hex=uuid.uuid4().hex)

    @classmethod
    def from_hex(cls, hex: str) -> Self:
        return cls(hex=hex)
