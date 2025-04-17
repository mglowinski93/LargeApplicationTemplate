from dataclasses import dataclass


@dataclass(frozen=True)
class EmailData:
    recipients: list[str]
    title: str
    content: str
