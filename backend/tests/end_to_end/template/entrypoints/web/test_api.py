from datetime import datetime, timedelta
from http import HTTPStatus

import pytest
from dateutil.parser import parse as parse_datetime
from freezegun import freeze_time

from modules.common import consts
from modules.common.adapters.notifications.notificators import DummyEmailNotificator
from modules.template.domain.value_objects import TemplateId

from ..... import fakers
from .....dtos import APIClientData
from ....consts import SQL_INJECTION_STRING
from ....utils import get_url

TEMPLATE_ROUTES = {
    "retrieve-template": "api.template-api.get_template_endpoint",
    "list-templates": "api.template-api.list_templates_endpoint",
    "create-template": "api.template-api.create_template_endpoint",
    "delete-template": "api.template-api.delete_template_endpoint",
    "set-template-value": "api.template-api.set_template_value_endpoint",
    "subtract-template-value": "api.template-api.subtract_template_value_endpoint",
}


def create_template_via_api(client: APIClientData) -> TemplateId:
    return TemplateId(
        client.client.post(  # type: ignore[index]
            get_url(
                app=client.client.application,
                routes=TEMPLATE_ROUTES,
                url_type="create-template",
            )
        ).json["id"]
    )


def timestamp_has_timezone_information(json_response) -> bool:
    timestamp = parse_datetime(json_response["timestamp"])
    return (
        timestamp.tzinfo is not None
        and timestamp.tzinfo.utcoffset(timestamp) is not None
    )


def test_get_template_endpoint_returns_template_data_when_specified_template_exist(
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = create_template_via_api(client)

    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="retrieve-template",
            path_parameters={"template_id": template_id},
        ),
    )

    # Then
    assert response.status_code == HTTPStatus.OK

    json_response = response.json
    assert json_response is not None
    assert "id" in json_response
    assert "value" in json_response
    assert TemplateId.from_hex(json_response["id"]) == template_id
    assert timestamp_has_timezone_information(json_response)


def test_get_template_endpoint_returns_404_when_specified_template_does_not_exist(
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = fakers.fake_template_id()

    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
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
    api_client = client.client
    template_id = "invalid-format-template-id"

    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
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


def test_list_templates_endpoint_returns_empty_list_when_no_template_exists(
    client: APIClientData,
):
    # Given
    api_client = client.client

    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
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
    api_client = client.client
    number_of_templates = 3
    for _ in range(number_of_templates):
        create_template_via_api(client)

    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
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
    api_client = client.client
    templates_number = 20
    pagination_offset = 1
    pagination_limit = 5
    for _ in range(templates_number):
        create_template_via_api(client)
    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
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
    assert json_response[consts.PAGINATION_TOTAL_COUNT_NAME] == templates_number
    assert consts.PAGINATION_NEXT_LINK_RELATION in json_response
    assert consts.PAGINATION_PREVIOUS_LINK_RELATION in json_response


def test_list_templates_endpoint_pagination_next_link(client: APIClientData):
    # Given
    api_client = client.client
    pagination_limit = 1

    template_2_id = create_template_via_api(client)
    template_1_id = create_template_via_api(client)

    # When and then
    response = api_client.get(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={
            consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME: 0,
            consts.PAGINATION_LIMIT_QUERY_PARAMETER_NAME: pagination_limit,
        },
    )

    assert response.status_code == HTTPStatus.OK
    json_response: dict = response.json  # type: ignore[assignment, no-redef]
    assert consts.PAGINATION_NEXT_LINK_RELATION in json_response
    assert json_response.get(consts.PAGINATION_PREVIOUS_LINK_RELATION) is None
    first_page_results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert len(first_page_results) == 1
    assert TemplateId(first_page_results[0]["id"]) == template_1_id

    # When and then
    response = api_client.get(json_response[consts.PAGINATION_NEXT_LINK_RELATION])

    assert response.status_code == HTTPStatus.OK
    json_response: dict = response.json  # type: ignore[assignment, no-redef]
    assert consts.PAGINATION_PREVIOUS_LINK_RELATION in json_response
    assert json_response.get(consts.PAGINATION_NEXT_LINK_RELATION) is None
    second_page_results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert len(second_page_results) == 1
    assert TemplateId(second_page_results[0]["id"]) == template_2_id


def test_list_templates_endpoint_handles_invalid_pagination_parameters(
    client: APIClientData,
):
    # Given
    api_client = client.client

    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={
            consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME: "invalid-offset",
        },
    )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST
    json_response: dict = response.json  # type: ignore[assignment]
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in json_response


def test_list_templates_endpoint_filtering_by_query(client: APIClientData):
    # Given
    api_client = client.client
    create_template_via_api(client)
    template_id = create_template_via_api(client)

    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
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
    assert len(results) == 1
    assert all(TemplateId.from_hex(item["id"]) == template_id for item in results)


def test_list_templates_endpoint_filtering_a_few_attributes(client: APIClientData):
    # Given
    api_client = client.client

    past_timestamp = datetime.now() - timedelta(days=1)
    with freeze_time(past_timestamp):
        create_template_via_api(client)
    future_timestamp = datetime.now() + timedelta(days=1)
    with freeze_time(future_timestamp):
        create_template_via_api(client)
    template_id = create_template_via_api(client)

    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={
            "timestamp_from": past_timestamp + timedelta(minutes=1),
            "timestamp_to": future_timestamp - timedelta(minutes=1),
        },
    )

    # Then
    assert response.status_code == HTTPStatus.OK

    json_response = response.json
    assert json_response is not None

    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert len(results) == 1
    assert all(TemplateId.from_hex(item["id"]) == template_id for item in results)


def test_list_templates_endpoint_skips_unsupported_filtering(client: APIClientData):
    # Given
    api_client = client.client
    create_template_via_api(client)
    template_id = create_template_via_api(client)

    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={"invalid-query-parameter": template_id},
    )

    # Then
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("order_by", ("timestamp", "-timestamp"))
def test_list_templates_endpoint_ordering(
    client: APIClientData,
    order_by: str,
):
    # Given
    api_client = client.client

    with freeze_time(datetime.now() - timedelta(days=1)):
        create_template_via_api(client)
    create_template_via_api(client)

    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={consts.ORDERING_QUERY_PARAMETER_NAME: order_by},
    )

    # Then
    compare_key = order_by[1:] if order_by.startswith("-") else order_by

    assert response.status_code == HTTPStatus.OK
    json_response: dict = response.json  # type: ignore[assignment]
    results = json_response[consts.PAGINATION_RESULTS_NAME]
    assert results == sorted(
        results,
        key=lambda item: item[compare_key],
        reverse=not order_by.startswith("-"),
    )


def test_list_templates_endpoint_skips_unsupported_ordering(
    client: APIClientData,
):
    # Given
    api_client = client.client

    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={consts.ORDERING_QUERY_PARAMETER_NAME: "not-existing-field"},
    )

    # Then
    assert response.status_code == HTTPStatus.OK


def test_list_templates_endpoint_escapes_query_parameters(client: APIClientData):
    # Given
    api_client = client.client

    # When
    response = api_client.get(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="list-templates",
        ),
        query_string={"query": SQL_INJECTION_STRING},
    )

    # Then
    assert response.status_code == HTTPStatus.OK


def test_create_template_endpoint_creates_template(
    client: APIClientData,
):
    # Given
    api_client = client.client

    # When
    response = api_client.post(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="create-template",
        )
    )

    # Then
    json_response = response.json
    assert json_response is not None
    assert response.status_code == HTTPStatus.CREATED
    assert "id" in json_response
    assert "value" not in json_response
    assert timestamp_has_timezone_information(json_response)


def test_delete_template_endpoint_deletes_template(
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = create_template_via_api(client)

    # When
    response = api_client.delete(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="delete-template",
            path_parameters={"template_id": template_id},
        )
    )

    # Then
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.json is None


def test_delete_template_endpoint_returns_404_when_specified_template_does_not_exist(
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = fakers.fake_template_id()

    # When
    response = api_client.delete(
        get_url(
            app=api_client.application,
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


def test_set_template_value_endpoint_sets_template_value_when_specified_template_exists(  # noqa: E501
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = create_template_via_api(client)
    template_value = fakers.fake_template_value().value

    # When
    response = api_client.patch(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )

    # Then
    assert response.status_code == HTTPStatus.OK

    response = api_client.get(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="retrieve-template",
            path_parameters={"template_id": template_id},
        )
    )

    assert response.status_code == HTTPStatus.OK

    json_response = response.json
    assert json_response is not None
    assert json_response["value"] == template_value
    assert timestamp_has_timezone_information(json_response)

    assert DummyEmailNotificator.total_emails_sent == 1


def test_set_template_value_endpoint_returns_404_when_specified_template_does_not_exists(  # noqa: E501
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = fakers.fake_template_id()
    template_value = fakers.fake_template_value().value

    # When
    response = api_client.patch(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in response.json
    assert not DummyEmailNotificator.total_emails_sent


def test_set_template_value_endpoint_returns_400_when_template_id_has_invalid_format(
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = "invalid-format-template-id"
    template_value = fakers.fake_template_value().value

    # When
    response = api_client.patch(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST

    json_response = response.json
    assert json_response is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in json_response

    assert not DummyEmailNotificator.total_emails_sent


def test_set_template_value_endpoint_returns_400_when_missing_parameters(
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = create_template_via_api(client)

    # When
    response = api_client.patch(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={},
    )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST

    json_response = response.json
    assert json_response is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in json_response

    assert not DummyEmailNotificator.total_emails_sent


def test_subtract_template_value_endpoint_subtracts_template_value(
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = create_template_via_api(client)
    template_value = fakers.fake_template_value().value
    subtraction_value = template_value - 1

    # When
    response = api_client.patch(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )

    assert response.status_code == HTTPStatus.OK

    response = api_client.post(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="subtract-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": subtraction_value},
    )

    assert response.status_code == HTTPStatus.OK

    # Then
    response = api_client.get(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="retrieve-template",
            path_parameters={"template_id": template_id},
        )
    )

    assert response.status_code == HTTPStatus.OK

    json_response = response.json
    assert json_response is not None
    assert json_response["value"] == template_value - subtraction_value
    assert timestamp_has_timezone_information(json_response)

    assert DummyEmailNotificator.total_emails_sent == 1


def test_subtract_template_value_endpoint_returns_404_when_specified_template_does_not_exists(  # noqa: E501
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = fakers.fake_template_id()
    value = fakers.fake_template_value().value

    # When
    response = api_client.post(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="subtract-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": value},
    )

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in response.json
    assert not DummyEmailNotificator.total_emails_sent


def test_subtract_template_value_endpoint_returns_400_when_template_id_has_invalid_format(  # noqa: E501
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = "invalid-format-template-id"
    value = fakers.fake_template_value().value

    # When
    response = api_client.post(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="subtract-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": value},
    )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST

    json_response = response.json
    assert json_response is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in json_response

    assert not DummyEmailNotificator.total_emails_sent


def test_subtract_template_value_endpoint_returns_400_when_missing_parameters(
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = create_template_via_api(client)
    template_value = fakers.fake_template_value().value

    response = api_client.patch(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )
    assert response.status_code == HTTPStatus.OK

    # When
    response = api_client.post(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="subtract-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={},
    )

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST

    json_response = response.json
    assert json_response is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in json_response

    assert DummyEmailNotificator.total_emails_sent == 1


def test_subtract_value_endpoint_returns_422_when_subtraction_value_is_greater_or_equal_template_value(  # noqa: E501
    client: APIClientData,
):
    # Given
    api_client = client.client
    template_id = create_template_via_api(client)
    template_value = fakers.fake_template_value().value

    response = api_client.patch(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="set-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": template_value},
    )
    assert response.status_code == HTTPStatus.OK

    # When
    subtraction_value = template_value
    response = api_client.post(
        get_url(
            app=api_client.application,
            routes=TEMPLATE_ROUTES,
            url_type="subtract-template-value",
            path_parameters={"template_id": template_id},
        ),
        json={"value": subtraction_value},
    )

    # Then
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    json_response = response.json
    assert json_response is not None
    assert consts.ERROR_RESPONSE_KEY_DETAILS_NAME in json_response

    assert DummyEmailNotificator.total_emails_sent == 1
