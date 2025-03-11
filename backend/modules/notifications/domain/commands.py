from dataclasses import dataclass

from modules.common.domain.commands import DomainCommand


@dataclass(frozen=True)
class SendEmail(DomainCommand):
    recipients: list[str]
    title: str
    content: str
