from flask.testing import FlaskClient
from apps.template_app.domain.entities import Template as TemplateEntity


def test_get_template_returns_200_when_template_exists(
    client: FlaskClient, template_entity: TemplateEntity
):
    pass
