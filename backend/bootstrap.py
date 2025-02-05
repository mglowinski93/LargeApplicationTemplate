import logging
import os
import signal
import sys
from typing import Optional

import inject
from flask import Blueprint
from flasgger import Swagger
from flask import Flask

from config import config, swagger_template, swagger_config, Config
from modules.common.adapters.task_dispatchers import CeleryTaskDispatcher
from modules.common.database import initialize_database
from modules.template_module.services import SqlAlchemyTemplatesUnitOfWork


def get_configuration(environment_name: Optional[str] = None) -> Config:
    if environment_name is None:
        environment_name = os.environ["ENVIRONMENT"]
    return config[environment_name]()


def inject_config(binder):
    binder.bind_to_constructor("templates_unit_of_work", SqlAlchemyTemplatesUnitOfWork)
    binder.bind_to_constructor("main_task_dispatcher", CeleryTaskDispatcher)


def close_app_cleanup():
    """
    Add here action to be performed before application shutdown.
    """

    pass


def create_app(environment_name: Optional[str] = None) -> Flask:
    """
    Set up here the initial state, configurations, and dependencies of an application.
    """

    configuration = get_configuration(environment_name)

    app = Flask(__name__)
    app.config.from_object(configuration)
    configuration.init_app(app)
    app.url_map.strict_slashes = False

    inject.configure(inject_config)

    initialize_database(configuration.database_url)

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

    from modules.template_module.entrypoints.web import (  # noqa: E402
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
