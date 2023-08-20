import os

from flask import jsonify, Blueprint
from flasgger import Swagger
from flask import Flask

from config import config, swagger_template, swagger_config


app = Flask(__name__)
environment_name = os.environ["ENVIRONMENT"]
app.config.from_object(config[environment_name])
config[environment_name].init_app(app)

swagger = Swagger(template=swagger_template, config=swagger_config)
swagger.init_app(app)

# START OF BLUEPRINT REGISTRATION
main_api_blueprint = Blueprint("api", __name__)

from apps.template_app.entrypoints.web import (  # noqa: E402
    api_blueprint as template_api_blueprint,
)

main_api_blueprint.register_blueprint(template_api_blueprint, url_prefix="/template")

app.register_blueprint(main_api_blueprint, url_prefix="/api")
# END OF BLUEPRINT REGISTRATION


@app.route("/health-check", strict_slashes=False)
def health_check():
    """
    file: ./swagger_files/health_check_endpoint.yml
    """

    return jsonify(
        {
            "health": "Running",
        }
    )
