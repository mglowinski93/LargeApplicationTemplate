import logging
import os
import signal
import sys
from typing import Optional

from flask import Blueprint
from flasgger import Swagger
from flask import Flask

from apps.template_app.adapters.repositories.sqlalchemy.orm import (
    clear_mappers as clear_template_mappers,
    start_mappers as start_template_mappers,
)
from apps.common.database import initialize_database
from config import config, swagger_template, swagger_config, Config


def get_configuration(environment_name: Optional[str] = None) -> Config:
    if environment_name is None:
        environment_name = os.environ["ENVIRONMENT"]
    return config[environment_name]()


def close_application_cleanup():
    clear_template_mappers()


def create_app(environment_name: Optional[str] = None) -> Flask:
    """
    Set up here the initial state, configurations, and dependencies of an application.
    """

    configuration = get_configuration(environment_name)

    app = Flask(__name__)
    app.config.from_object(configuration)
    configuration.init_app(app)
    app.url_map.strict_slashes = False

    initialize_database(configuration.database_url)
    start_template_mappers()

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

    from apps.template_app.entrypoints.web import (  # noqa: E402
        api_blueprint as template_api_blueprint,
    )

    main_api_blueprint.register_blueprint(
        template_api_blueprint, url_prefix="/templates"
    )

    app.register_blueprint(main_api_blueprint, url_prefix="/api")
    # END OF BLUEPRINT REGISTRATION

    def closing_application_handler(signum, frame):
        close_application_cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, closing_application_handler)
    signal.signal(signal.SIGTERM, closing_application_handler)

    return app
