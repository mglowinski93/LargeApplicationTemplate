from collections import deque
from typing import Any, Callable, Sequence, Type

from ..template.domain.entities import Template
from .domain.commands import DomainCommand
from .domain.events import DomainEvent

Message = DomainEvent | DomainCommand


class MessageBus:
    def __init__(
        self,
        event_handlers: dict[Type[DomainEvent], list[Callable]],
        command_handlers: dict[Type[DomainCommand], Callable],
    ):
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.queue: deque[Message] = deque()

    def handle(self, messages: Sequence[Message]) -> None:
        self.queue.extend(messages)

        while self.queue:
            message = self.queue.popleft()

            if isinstance(message, DomainEvent):
                self.handle_event(message)
            elif isinstance(message, DomainCommand):
                self.handle_command(message)
            else:
                raise NotImplementedError(
                    f"Message type '{type(message)}' not supported."
                )

    def handle_event(self, event: DomainEvent):
        try:
            handlers = self.event_handlers[type(event)]
        except KeyError as err:
            raise NotImplementedError(
                f"Event type '{type(event)}' not supported."
            ) from err

        for handler in handlers:
            result = handler(event)

            self._collect_new_messages(result)

    def handle_command(self, command: DomainCommand):
        try:
            result = self.command_handlers[type(command)](command)
        except KeyError as err:
            raise NotImplementedError(
                f"Command type '{type(command)}' not supported."
            ) from err

        self._collect_new_messages(result)

    def _collect_new_messages(self, result: Any):
        if isinstance(result, Message):
            self.queue.append(result)
        elif isinstance(result, Sequence):
            self.queue.extend(
                message for message in result if isinstance(message, Message)
            )
        elif isinstance(result, Template):
            self.queue.extend(
                message for message in result.messages if isinstance(message, Message)
            )
