from datetime import datetime, timedelta
from dateutil.parser import parse as parse_datetime
from http import HTTPStatus
from typing import Any


from flask.testing import FlaskClient
from freezegun import freeze_time

from apps.common import consts
from ....utils import get_site_url
from .....factories import fake_template_id, fake_template_value


TEMPLATES_ROUTES = {
    "retrieve-template": "api.template-api.get_template_endpoint",
    "list-templates": "api.template-api.list_templates_endpoint",
    "create-template": "api.template-api.create_templates_endpoint",
    "set-template-value": "api.template-api.set_template_value_endpoint",
}


def test_list_templates_returns_empty_list_when_no_template_exists(
    client: FlaskClient,
):
    # When
    response = client.get(
        get_site_url(
            app=client.application, routes=TEMPLATES_ROUTES, url_type="list-templates"
        )
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    json_response: dict[str, Any] = response.json  # type: ignore
    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert isinstance(results, list)
    assert not results
    assert json_response[consts.PAGINATION_TOTAL_COUNT_NAME] == 0


def test_list_templates_returns_templates_data_when_templates_exist(
    client: FlaskClient,
):
    # Given
    number_of_templates = 3
    for _ in range(number_of_templates):
        client.post(
            get_site_url(
                app=client.application,
                routes=TEMPLATES_ROUTES,
                url_type="create-template",
            )
        )

    # When
    response = client.get(
        get_site_url(
            app=client.application, routes=TEMPLATES_ROUTES, url_type="list-templates"
        )
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    json_response: dict[str, Any] = response.json  # type: ignore
    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert isinstance(results, list)
    assert json_response[consts.PAGINATION_TOTAL_COUNT_NAME] == number_of_templates


def test_list_templates_pagination(client: FlaskClient):
    # Given
    number_of_templates = 20
    for _ in range(number_of_templates):
        client.post(
            get_site_url(
                app=client.application,
                routes=TEMPLATES_ROUTES,
                url_type="create-template",
            )
        )

    # When
    response = client.get(
        get_site_url(
            app=client.application, routes=TEMPLATES_ROUTES, url_type="list-templates"
        ),
        query_string={
            consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME: 1,
            consts.PAGINATION_LIMIT_QUERY_PARAMETER_NAME: 5,
        },
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    json_response: dict[str, Any] = response.json  # type: ignore
    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert len(results) == 5
    assert json_response[consts.PAGINATION_TOTAL_COUNT_NAME] == number_of_templates
    assert consts.PAGINATION_NEXT_LINK_RELATION in json_response
    assert consts.PAGINATION_PREVIOUS_LINK_RELATION in json_response


def test_list_templates_ordering(client: FlaskClient):
    # Given
    with freeze_time(datetime.now() - timedelta(days=1)):
        client.post(
            get_site_url(
                app=client.application,
                routes=TEMPLATES_ROUTES,
                url_type="create-template",
            )
        )
    client.post(
        get_site_url(
            app=client.application,
            routes=TEMPLATES_ROUTES,
            url_type="create-template",
        )
    )

    response = client.get(
        get_site_url(
            app=client.application, routes=TEMPLATES_ROUTES, url_type="list-templates"
        ),
        query_string={consts.ORDERING_QUERY_PARAMETER_NAME: "-timestamp"},
    )
    assert response.status_code == HTTPStatus.OK
    results = response.json[consts.PAGINATION_RESULTS_NAME]  # type: ignore
    assert parse_datetime(results[0]["timestamp"]) > parse_datetime(
        results[1]["timestamp"]
    )

    response = client.get(
        get_site_url(
            app=client.application, routes=TEMPLATES_ROUTES, url_type="list-templates"
        ),
        query_string={consts.ORDERING_QUERY_PARAMETER_NAME: "timestamp"},
    )
    assert response.status_code == HTTPStatus.OK
    results = response.json[consts.PAGINATION_RESULTS_NAME]  # type: ignore
    assert parse_datetime(results[0]["timestamp"]) < parse_datetime(
        results[1]["timestamp"]
    )


def test_list_templates_filtering(client: FlaskClient):
    # Given
    client.post(
        get_site_url(
            app=client.application,
            routes=TEMPLATES_ROUTES,
            url_type="create-template",
        )
    )
    template_value = fake_template_value().value

    template_id = client.post(  # type: ignore
        get_site_url(
            app=client.application, routes=TEMPLATES_ROUTES, url_type="create-template"
        )
    ).json["id"]
    client.patch(
        get_site_url(
            app=client.application,
            routes=TEMPLATES_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )

    # When
    response = client.get(
        get_site_url(
            app=client.application, routes=TEMPLATES_ROUTES, url_type="list-templates"
        ),
        query_string={"value": template_value},
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    results = response.json[consts.PAGINATION_RESULTS_NAME]  # type: ignore
    assert all(item["value"] == template_value for item in results)


def test_get_template_returns_template_data_when_specified_template_exist(
    client: FlaskClient,
):
    # Given
    template_id = client.post(  # type: ignore
        get_site_url(
            app=client.application, routes=TEMPLATES_ROUTES, url_type="create-template"
        )
    ).json["id"]

    # When
    response = client.get(
        get_site_url(
            app=client.application,
            routes=TEMPLATES_ROUTES,
            url_type="retrieve-template",
            path_parameters={"template_id": template_id},
        ),
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json["id"] == template_id  # type: ignore


def test_get_template_returns_404_when_specified_template_doesnt_exist(
    client: FlaskClient,
):
    # Given
    template_id = fake_template_id()

    # When
    response = client.get(
        get_site_url(
            app=client.application,
            routes=TEMPLATES_ROUTES,
            url_type="retrieve-template",
            path_parameters={"template_id": template_id},
        ),
    )

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in response.json  # type: ignore


def test_get_template_returns_400_when_template_id_has_invalid_format(
    client: FlaskClient,
):
    # Given
    template_id = "invalid-format-template-id"

    # When
    response = client.get(
        get_site_url(
            app=client.application,
            routes=TEMPLATES_ROUTES,
            url_type="retrieve-template",
            path_parameters={"template_id": template_id},
        ),
    )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in response.json  # type: ignore


def test_create_template_creates_template_and_returns_data(
    client: FlaskClient,
):
    # When
    response = client.post(
        get_site_url(
            app=client.application, routes=TEMPLATES_ROUTES, url_type="create-template"
        )
    )

    # Then
    json_response: dict[str, Any] = response.json  # type: ignore
    assert response.status_code == HTTPStatus.CREATED
    assert "id" in json_response
    assert "value" in json_response
    assert json_response["value"] is None


def test_set_template_value_sets_template_value_and_returns_no_data_when_specified_template_exists(  # noqa: E501
    client: FlaskClient,
):
    # Given
    template_id = client.post(  # type: ignore
        get_site_url(
            app=client.application, routes=TEMPLATES_ROUTES, url_type="create-template"
        )
    ).json["id"]
    template_value = fake_template_value().value

    # When
    response = client.patch(
        get_site_url(
            app=client.application,
            routes=TEMPLATES_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    assert (
        client.get(  # type: ignore
            get_site_url(
                app=client.application,
                routes=TEMPLATES_ROUTES,
                url_type="retrieve-template",
                path_parameters={"template_id": template_id},
            ),
        ).json["value"]
        == template_value
    )


def test_set_template_value_returns_404_when_specified_template_doesnt_exists(
    client: FlaskClient,
):
    # Given
    template_id = fake_template_id()
    template_value = fake_template_value().value

    # When
    response = client.patch(
        get_site_url(
            app=client.application,
            routes=TEMPLATES_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in response.json  # type: ignore


def test_set_template_value_returns_400_when_template_id_has_invalid_format(
    client: FlaskClient,
):
    # Given
    template_id = "invalid-format-template-id"
    template_value = fake_template_value().value

    # When
    response = client.patch(
        get_site_url(
            app=client.application,
            routes=TEMPLATES_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in response.json  # type: ignore


def test_set_template_value_returns_400_when_missing_parameters(
    client: FlaskClient,
):
    # Given
    template_id = fake_template_id()

    # When
    response = client.patch(
        get_site_url(
            app=client.application,
            routes=TEMPLATES_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={},
    )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in response.json  # type: ignore
