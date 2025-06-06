import inspect
import logging
import os
import signal
import sys
from collections import defaultdict
from typing import Callable

import inject
from flasgger import Swagger
from flask import Blueprint, Flask

from config import Config, config, swagger_config, swagger_template
from modules.common import message_bus as common_message_bus
from modules.common.adapters.notifications import DummyEmailNotificator
from modules.common.adapters.task_dispatchers import CeleryTaskDispatcher
from modules.common.database import initialize_database_sessions
from modules.common.domain.events import DomainEvent
from modules.template import adapters as template_adapters
from modules.template.services import handlers as template_handlers


def get_configuration(environment_name: str | None = None) -> Config:
    if environment_name is None:
        environment_name = os.environ["ENVIRONMENT"]
    return config[environment_name]()


def inject_dependencies_into_handlers(handler: Callable, bindings: dict) -> Callable:
    all_function_parameters = inspect.signature(handler).parameters
    dependencies = {
        parameter_name: bindings[parameter_name]()
        for parameter_name in all_function_parameters.keys()
        if parameter_name in bindings
    }

    # fmt: off
    def wrapper(*args, **kwargs):
        try:
            return handler(
                **dependencies,
                **{
                    parameter_name: args[index]
                    for index, (parameter_name, parameter_value) in enumerate(
                        {
                            parameter_name: parameter_value
                            for parameter_name, parameter_value in 
                            all_function_parameters.items()
                            if parameter_name not in dependencies
                        }.items()
                    )
                },
                **kwargs,
            )
        except IndexError as err:
            raise RuntimeError(
                f"Could not find dependencies to inject into {handler.__name__}."
            ) from err
    # fmt: on

    return wrapper


def inject_config(binder):
    binder.bind_to_constructor("main_task_dispatcher", CeleryTaskDispatcher)
    binder.bind_to_constructor("email_notificator", DummyEmailNotificator)
    binder.bind_to_constructor(
        "templates_unit_of_work", template_adapters.SqlAlchemyTemplatesUnitOfWork
    )
    binder.bind_to_constructor(
        "templates_query_repository",
        template_adapters.SqlAlchemyTemplatesQueryRepository,
    )
    _message_bus = common_message_bus.MessageBus(
        event_handlers={},
        command_handlers={},
    )
    binder.bind(
        "message_bus",
        _message_bus,
    )
    _message_bus.event_handlers = _parse_event_handlers(
        handlers=[
            template_handlers.EVENT_HANDLERS,
        ],
        bindings=binder._bindings,
    )
    _message_bus.command_handlers = {
        command: inject_dependencies_into_handlers(
            handler=handler, bindings=binder._bindings
        )
        for handler_ in [
            template_handlers.COMMAND_HANDLERS,
        ]
        for command, handler in handler_.items()
    }


def _parse_event_handlers(
    handlers: list[
        dict[
            type[DomainEvent],
            list[Callable],
        ]
    ],
    bindings: dict,
) -> dict:
    results: dict[type[DomainEvent], list[Callable]] = defaultdict(list)

    for _handlers in handlers:
        for key, _event_handlers in _handlers.items():
            results[key].extend(
                inject_dependencies_into_handlers(
                    handler=_event_handler, bindings=bindings
                )
                for _event_handler in _event_handlers
            )

    return results


def close_app_cleanup():
    """
    Add here action to be performed before application shutdown.
    """

    pass


def create_app(environment_name: str | None = None) -> Flask:
    """
    Set up here the initial state, configurations, and dependencies of an application.
    """

    configuration = get_configuration(environment_name)

    app = Flask(__name__)
    app.config.from_object(configuration)
    configuration.init_app(app)
    app.url_map.strict_slashes = False

    inject.configure(inject_config)

    initialize_database_sessions(configuration.database_url)

    logging.basicConfig(
        level=logging.getLevelName(app.config["LOG_LEVEL"]),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if app.config["SWAGGER_ENABLED"]:
        swagger = Swagger(template=swagger_template, config=swagger_config)
        swagger.init_app(app)

    # START OF BLUEPRINT REGISTRATION
    main_api_blueprint = Blueprint("api", __name__)

    from modules.template.entrypoints.web import (  # noqa: E402
        api_blueprint as template_api_blueprint,
    )

    main_api_blueprint.register_blueprint(
        template_api_blueprint, url_prefix="/templates"
    )

    app.register_blueprint(main_api_blueprint, url_prefix="/api")
    # END OF BLUEPRINT REGISTRATION

    def closing_application_handler(signum, frame):
        close_app_cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, closing_application_handler)
    signal.signal(signal.SIGTERM, closing_application_handler)

    return app
