from dataclasses import dataclass

from flask.testing import FlaskClient


@dataclass
class APIClientData:
    client: FlaskClient
