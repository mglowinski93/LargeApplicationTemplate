import pytest
from pytest_mock import MockFixture

from modules.common import message_bus as common_message_bus
from modules.common.domain import (
    events as common_domain_events,
    commands as common_domain_commands,
)


def test_message_bus_has_empty_queue_for_new_instance(
    message_bus: common_message_bus.MessageBus,
):
    # Then
    assert not message_bus.queue


def test_message_bus_uses_handlers_assigned_to_event(
    mocker: MockFixture,
    message_bus: common_message_bus.MessageBus,
):
    # Given
    event = common_domain_events.DomainEvent()

    handlers = [mocker.Mock(), mocker.Mock()]
    message_bus.event_handlers = {type(event): handlers}

    # When
    message_bus.handle([event])

    # Then
    for handler in handlers:
        handler.assert_called_once()
    assert not message_bus.queue


def test_message_bus_uses_handler_assigned_to_command(
    mocker: MockFixture,
    message_bus: common_message_bus.MessageBus,
):
    # Given
    command = common_domain_commands.DomainCommand()
    handler = mocker.Mock()
    message_bus.command_handlers = {
        type(command): handler,
    }

    # When
    message_bus.handle([command])

    # Then
    handler.assert_called_once()
    assert not message_bus.queue


def test_message_bus_raises_exception_for_unsupported_message_type(
    message_bus: common_message_bus.MessageBus,
):
    # When
    with pytest.raises(NotImplementedError):
        message_bus.handle([common_domain_events.DomainEvent()])


@pytest.mark.parametrize(
    "return_value",
    (
        common_domain_events.DomainEvent(),
        [common_domain_events.DomainEvent()],
    ),
)
def test_message_bus_collects_new_messages_from_handlers(
    mocker: MockFixture,
    message_bus: common_message_bus.MessageBus,
    return_value: (
        common_domain_events.DomainEvent | list[common_domain_events.DomainEvent]
    ),
):
    # Given
    class SubEvent(common_domain_events.DomainEvent):
        pass

    sub_event = SubEvent()
    sub_event_handler = mocker.Mock(return_value=return_value)
    event_handler = mocker.Mock()
    message_bus.event_handlers = {
        SubEvent: [sub_event_handler],
        common_domain_events.DomainEvent: [event_handler],
    }

    # When
    message_bus.handle([sub_event])

    # Then
    assert not message_bus.queue
    sub_event_handler.assert_called_once()
    event_handler.assert_called_once()


def test_message_bus_does_not_execute_handler_when_no_message_returned_by_other_handler(
    mocker: MockFixture,
    message_bus: common_message_bus.MessageBus,
):
    # Given
    class SubEvent(common_domain_events.DomainEvent):
        pass

    sub_event = SubEvent()
    sub_event_handler = mocker.Mock(return_value=None)
    event_handler = mocker.Mock()
    message_bus.event_handlers = {
        SubEvent: [sub_event_handler],
        common_domain_events.DomainEvent: [event_handler],
    }

    # When
    message_bus.handle([sub_event])

    # Then
    assert not message_bus.queue
    sub_event_handler.assert_called_once()
    event_handler.assert_not_called()
