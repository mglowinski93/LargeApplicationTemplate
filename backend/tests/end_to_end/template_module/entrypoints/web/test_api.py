from datetime import datetime, timedelta
from http import HTTPStatus

from dateutil.parser import parse as parse_datetime
from freezegun import freeze_time

from modules.common import consts
from modules.common.adapters.notifications.notificators import DummyEmailNotificator

from .....dtos import APIClientData
from .....fakers import fake_template_id, fake_template_value
from ....utils import get_url

TEMPLATE_ROUTES = {
    "retrieve-template": "api.template-api.get_template_endpoint",
    "list-templates": "api.template-api.list_templates_endpoint",
    "create-template": "api.template-api.create_template_endpoint",
    "delete-template": "api.template-api.delete_template_endpoint",
    "set-template-value": "api.template-api.set_template_value_endpoint",
}


def test_list_templates_endpoint_returns_empty_list_when_no_template_exists(
    client: APIClientData,
):
    # When
    response = client.client.get(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        )
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    json_response = response.json
    assert json_response is not None
    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert isinstance(results, list)
    assert not results
    assert json_response[consts.PAGINATION_TOTAL_COUNT_NAME] == 0


def test_list_templates_endpoint_returns_templates_data_when_templates_exist(
    client: APIClientData,
):
    # Given
    number_of_templates = 3
    for _ in range(number_of_templates):
        client.client.post(
            get_url(
                app=client.client.application,
                routes=TEMPLATE_ROUTES,
                url_type="create-template",
            )
        )

    # When
    response = client.client.get(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        )
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    json_response = response.json
    assert json_response is not None
    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert isinstance(results, list)
    assert json_response[consts.PAGINATION_TOTAL_COUNT_NAME] == number_of_templates


def test_list_templates_endpoint_pagination(client: APIClientData):
    # Given
    number_of_templates = 20
    pagination_offset = 1
    pagination_limit = 5
    for _ in range(number_of_templates):
        client.client.post(
            get_url(
                app=client.client.application,
                routes=TEMPLATE_ROUTES,
                url_type="create-template",
            )
        )

    # When
    response = client.client.get(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={
            consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME: pagination_offset,
            consts.PAGINATION_LIMIT_QUERY_PARAMETER_NAME: pagination_limit,
        },
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    json_response = response.json
    assert json_response is not None
    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert len(results) == pagination_limit
    assert json_response[consts.PAGINATION_TOTAL_COUNT_NAME] == number_of_templates
    assert consts.PAGINATION_NEXT_LINK_RELATION in json_response
    assert consts.PAGINATION_PREVIOUS_LINK_RELATION in json_response


def test_list_templates_endpoint_ordering_timestamp(client: APIClientData):
    with freeze_time(datetime.now() - timedelta(days=1)):
        client.client.post(
            get_url(
                app=client.client.application,
                routes=TEMPLATE_ROUTES,
                url_type="create-template",
            )
        )
    client.client.post(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="create-template",
        )
    )

    response = client.client.get(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={consts.ORDERING_QUERY_PARAMETER_NAME: "-timestamp"},
    )
    assert response.status_code == HTTPStatus.OK
    json_response = response.json
    assert json_response is not None
    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert parse_datetime(results[0]["timestamp"]) > parse_datetime(
        results[1]["timestamp"]
    )

    response = client.client.get(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={consts.ORDERING_QUERY_PARAMETER_NAME: "timestamp"},
    )
    assert response.status_code == HTTPStatus.OK
    json_response = response.json
    assert json_response is not None
    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert parse_datetime(results[0]["timestamp"]) < parse_datetime(
        results[1]["timestamp"]
    )


def get_template_id(client: APIClientData) -> str:
    response = client.client.post(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="create-template",
        )
    )
    assert response.status_code == HTTPStatus.CREATED
    json_response = response.json
    assert json_response is not None and "id" in json_response
    return json_response["id"]


def test_list_templates_endpoint_ordering_value(
    client: APIClientData,
):
    templates = []
    values = ["a", "b"]
    for template_value in values:
        template_id = get_template_id(client)
        client.client.patch(
            get_url(
                app=client.client.application,
                routes=TEMPLATE_ROUTES,
                url_type="set-template-value",
                path_parameters={"template_id": template_id},
            ),
            json={"value": template_value},
        )
        templates.append(template_id)

    assert DummyEmailNotificator.total_emails_sent == values.__len__()

    response = client.client.get(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={consts.ORDERING_QUERY_PARAMETER_NAME: "-value"},
    )
    assert response.status_code == HTTPStatus.OK
    json_response = response.json
    assert json_response is not None
    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert results[0]["id"] == templates[1]
    assert results[1]["id"] == templates[0]

    response = client.client.get(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={consts.ORDERING_QUERY_PARAMETER_NAME: "value"},
    )
    assert response.status_code == HTTPStatus.OK
    json_response = response.json
    assert json_response is not None
    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert results[0]["id"] == templates[0]
    assert results[1]["id"] == templates[1]


def test_list_templates_endpoint_filtering_by_query(client: APIClientData):
    # Given
    client.client.post(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="create-template",
        )
    )
    template_id = get_template_id(client)

    # When
    response = client.client.get(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={"query": template_id},
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    json_response = response.json
    assert json_response is not None
    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert all(item["id"] == template_id for item in results)


def test_get_template_endpoint_returns_template_data_when_specified_template_exist(
    client: APIClientData,
):
    # Given
    template_id = get_template_id(client)

    # When
    response = client.client.get(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="retrieve-template",
            path_parameters={"template_id": template_id},
        ),
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    json_response = response.json
    assert json_response is not None
    assert json_response["id"] == template_id


def test_get_template_endpoint_returns_404_when_specified_template_doesnt_exist(
    client: APIClientData,
):
    # Given
    template_id = fake_template_id()

    # When
    response = client.client.get(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="retrieve-template",
            path_parameters={"template_id": template_id},
        ),
    )

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
    json_response = response.json
    assert json_response is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in json_response


def test_get_template_endpoint_returns_400_when_template_id_has_invalid_format(
    client: APIClientData,
):
    # Given
    template_id = "invalid-format-template-id"

    # Whenclient.
    response = client.client.get(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="retrieve-template",
            path_parameters={"template_id": template_id},
        ),
    )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST
    json_response = response.json
    assert json_response is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in json_response


def test_create_template_endpoint_creates_template_and_returns_data(
    client: APIClientData,
):
    # When
    response = client.client.post(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="create-template",
        )
    )

    # Then
    json_response = response.json
    assert json_response is not None
    assert response.status_code == HTTPStatus.CREATED
    assert "id" in json_response
    assert "value" in json_response
    assert json_response["value"] is None


def test_delete_template_endpoint_deletes_template(
    client: APIClientData,
):
    # Given
    template_id = get_template_id(client)

    # When
    response = client.client.delete(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="delete-template",
            path_parameters={"template_id": template_id},
        )
    )

    # Then
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.json is None


def test_delete_template_endpoint_returns_404_when_specified_template_doesnt_exist(
    client: APIClientData,
):
    # Given
    template_id = fake_template_id()

    # When
    response = client.client.delete(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="delete-template",
            path_parameters={"template_id": template_id},
        )
    )

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
    json_response = response.json
    assert json_response is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in json_response


def test_set_template_value_endpoint_sets_template_value_and_returns_no_data_when_specified_template_exists(  # noqa: E501
    client: APIClientData,
):
    # Given
    template_id = get_template_id(client)
    template_value = fake_template_value().value

    # When
    response = client.client.patch(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )

    # Then
    assert response.status_code == HTTPStatus.OK
    response = client.client.get(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="retrieve-template",
            path_parameters={"template_id": template_id},
        )
    )
    assert DummyEmailNotificator.total_emails_sent == 1
    assert response.status_code == HTTPStatus.OK
    assert response.json is not None
    assert response.json["value"] == template_value


def test_set_template_value_endpoint_returns_404_when_specified_template_doesnt_exists(
    client: APIClientData,
):
    # Given
    template_id = fake_template_id()
    template_value = fake_template_value().value

    # When
    response = client.client.patch(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )

    # Then
    assert DummyEmailNotificator.total_emails_sent == 0
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in response.json


def test_set_template_value_endpoint_returns_400_when_template_id_has_invalid_format(
    client: APIClientData,
):
    # Given
    template_id = "invalid-format-template-id"
    template_value = fake_template_value().value

    # When
    response = client.client.patch(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )

    # Then
    assert DummyEmailNotificator.total_emails_sent == 0
    assert response.status_code == HTTPStatus.BAD_REQUEST
    json_response = response.json
    assert json_response is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in json_response


def test_set_template_value_endpoint_returns_400_when_missing_parameters(
    client: APIClientData,
):
    # Given
    template_id = fake_template_id()

    # When
    response = client.client.patch(
        get_url(
            app=client.client.application,
            routes=TEMPLATE_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={},
    )

    # Then
    assert DummyEmailNotificator.total_emails_sent == 0
    assert response.status_code == HTTPStatus.BAD_REQUEST
    json_response = response.json
    assert json_response is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in json_response
