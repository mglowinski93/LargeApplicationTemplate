from flask import Blueprint


api_blueprint = Blueprint("template-api", __name__)

# Ensure that the views file was imported
# after creating blueprint to properly register endpoints.
# More details can be found here:
# https://flask.palletsprojects.com/en/2.0.x/patterns/packages/#simple-packages.
from . import api  # noqa: E402,F401
