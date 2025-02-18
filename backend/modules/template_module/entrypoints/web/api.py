import logging
from http import HTTPStatus
from typing import Optional
from uuid import UUID

import inject
from flask import jsonify, make_response, request
from werkzeug.datastructures import MultiDict

from . import api_blueprint
from . import forms as template_forms
from ... import services
from ...domain.commands.template import SetTemplateValue, CreateTemplate, DeleteTemplate
from ...domain import exceptions as domain_exceptions, value_objects
from ...domain.ports import exceptions as ports_exceptions, dtos as ports_dtos
from ....common.message_bus import MessageBus
from ...adapters.repositories.sqlalchemy import SqlAlchemyTemplateQueryRepository
from ....common import dtos as common_dtos
from ....common.entrypoints.web import forms as common_forms
from ....common import consts, docstrings, pagination as pagination_utils


logger = logging.getLogger(__name__)


@api_blueprint.route("/<template_id>", methods=["GET"])
@docstrings.inject_parameter_info_doc_strings(consts.SWAGGER_FILES)
@inject.params(query_repository="templates_query_repository")
def get_template_endpoint(
    template_id: str, query_repository: SqlAlchemyTemplateQueryRepository
):
    """
    file: {0}/template_endpoints/get_template.yml
    """

    logger.debug("Getting data for template '%s'.", template_id)

    try:
        template_id: value_objects.TEMPLATE_ID_TYPE = UUID(template_id)  # type: ignore
    except ValueError:
        logger.warning("Invalid template ID format: '%s'.", template_id)
        return make_response(
            jsonify(
                {consts.ERROR_RESPONSE_KEY_DETAILS_NAME: "Invalid template ID format."}
            ),
            HTTPStatus.BAD_REQUEST,
        )

    try:
        template = services.get_template(
            query_repository=query_repository,
            template_id=template_id,  # type: ignore
        )
        logger.debug("Template '%s' found.", template_id)
    except ports_exceptions.TemplateDoesNotExist:
        logger.warning("Template '%s' does not exist.", template_id)
        return make_response(
            jsonify({consts.ERROR_RESPONSE_KEY_DETAILS_NAME: "Template not found."}),
            HTTPStatus.NOT_FOUND,
        )

    return make_response(jsonify(template.serialize()), HTTPStatus.OK)


@api_blueprint.route("/", methods=["GET"])
@docstrings.inject_parameter_info_doc_strings(consts.SWAGGER_FILES)
@inject.params(query_repository="templates_query_repository")
def list_templates_endpoint(query_repository: SqlAlchemyTemplateQueryRepository):
    """
    file: {0}/template_endpoints/list_templates.yml
    """

    logger.debug("Listing all templates.")

    query_params = request.args
    logger.debug("Query params are: '%s'.", query_params)

    try:
        pagination = pagination_utils.Pagination(
            offset=int(
                query_params.get(consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME, 0)
            ),
            records_per_page=int(
                query_params.get(consts.PAGINATION_LIMIT_QUERY_PARAMETER_NAME, 10)
            ),
        )
    except ValueError as err:
        logger.warning("Invalid pagination parameters: '%s'.", err)
        return make_response(
            jsonify({consts.ERROR_RESPONSE_KEY_DETAILS_NAME: str(err)}),
            HTTPStatus.BAD_REQUEST,
        )

    form = template_forms.TemplatesFiltersForm(
        data=query_params,
        meta={"csrf": False},
    )
    if not form.validate():
        return make_response(
            jsonify({consts.ERROR_RESPONSE_KEY_DETAILS_NAME: form.errors}),
            HTTPStatus.BAD_REQUEST,
        )

    filters = ports_dtos.TemplatesFilters(
        value=form.value.data,
        query=form.query.data,
        timestamp_from=form.timestamp_from.data,
        timestamp_to=form.timestamp_to.data,
    )

    ordering: Optional[list[common_dtos.Ordering]] = (
        common_forms.OrderingForm(
            data=request.args,
            meta={"csrf": False},
        ).create_ordering()
        if consts.ORDERING_QUERY_PARAMETER_NAME in query_params
        else None
    )

    templates, all_templates_count = services.list_templates(
        query_repository=query_repository,
        filters=filters,
        ordering=ordering,
        pagination=pagination,
    )

    return make_response(
        jsonify(
            {
                consts.PAGINATION_TOTAL_COUNT_NAME: all_templates_count,
                consts.PAGINATION_NEXT_LINK_RELATION: pagination_utils.get_next_pagination_link(  # noqa: E501
                    url=request.url,
                    offset=pagination.offset,
                    records_per_page=pagination.records_per_page,
                    all_records_count=all_templates_count,
                ),
                consts.PAGINATION_PREVIOUS_LINK_RELATION: pagination_utils.get_previous_pagination_link(  # noqa: E501
                    url=request.url,
                    offset=pagination.offset,
                    records_per_page=pagination.records_per_page,
                ),
                consts.PAGINATION_RESULTS_NAME: [
                    template.serialize() for template in templates
                ],
            }
        ),
        HTTPStatus.OK,
    )


@api_blueprint.route("/", methods=["POST"])
@docstrings.inject_parameter_info_doc_strings(consts.SWAGGER_FILES)
@inject.params(message_bus="message_bus")
def create_template_endpoint(message_bus: MessageBus):
    """
    file: {0}/template_endpoints/create_template.yml
    """

    logger.info("Creating a new template.")

    template = message_bus.handle(CreateTemplate())

    logger.info("Template '%s' created.", template.id)

    return make_response(jsonify(template.serialize()), HTTPStatus.CREATED)


@api_blueprint.route("/<template_id>", methods=["DELETE"])
@docstrings.inject_parameter_info_doc_strings(consts.SWAGGER_FILES)
@inject.params(message_bus="message_bus")
def delete_template_endpoint(message_bus: MessageBus, template_id: str):
    """
    file: {0}/template_endpoints/delete_template.yml
    """

    logger.info("Deleting template '%s'.", template_id)

    try:
        template_id: value_objects.TEMPLATE_ID_TYPE = UUID(template_id)  # type: ignore
    except ValueError:
        logger.warning("Invalid template ID format: '%s'.", template_id)
        return make_response(
            jsonify(
                {consts.ERROR_RESPONSE_KEY_DETAILS_NAME: "Invalid template ID format."}
            ),
            HTTPStatus.BAD_REQUEST,
        )

    try:
        message_bus.handle(DeleteTemplate(template_id=template_id))
        logger.debug("Template '%s' found.", template_id)
    except ports_exceptions.TemplateDoesNotExist:
        logger.warning("Template '%s' does not exist.", template_id)
        return make_response(
            jsonify({consts.ERROR_RESPONSE_KEY_DETAILS_NAME: "Template not found."}),
            HTTPStatus.NOT_FOUND,
        )

    return make_response("", HTTPStatus.NO_CONTENT)


@api_blueprint.route("/<template_id>", methods=["PATCH"])
@docstrings.inject_parameter_info_doc_strings(consts.SWAGGER_FILES)
@inject.params(message_bus="message_bus")
def set_template_value_endpoint(message_bus: MessageBus, template_id: str):
    """
    file: {0}/template_endpoints/set_template_value.yml
    """

    logger.info("Setting value for template '%s'.", template_id)

    try:
        template_id: value_objects.TEMPLATE_ID_TYPE = UUID(template_id)  # type: ignore
    except ValueError:
        logger.warning("Invalid template ID format: '%s'.", template_id)
        return make_response(
            jsonify(
                {consts.ERROR_RESPONSE_KEY_DETAILS_NAME: "Invalid template ID format."}
            ),
            HTTPStatus.BAD_REQUEST,
        )

    form = template_forms.SetTemplateValueForm(
        formdata=MultiDict(request.get_json(force=True, silent=True)),
        meta={"csrf": False},
    )
    if not form.validate():
        logger.warning("Request can't be handled, due to invalid input data.")
        return make_response(
            jsonify({consts.ERROR_RESPONSE_KEY_DETAILS_NAME: form.errors}),
            HTTPStatus.BAD_REQUEST,
        )

    template_value = form.value.data

    try:
        logger.info("Setting value for template '%s'.", template_id)
        message_bus.handle(
            SetTemplateValue(template_id=template_id, value=template_value)
        )
        logger.info("Value '%s' set for template '%s'.", template_value, template_id)
    except domain_exceptions.InvalidTemplateValue:
        logger.warning(
            "Invalid value '%s' for template '%s'.", template_value, template_id
        )
        return make_response(
            jsonify({consts.ERROR_RESPONSE_KEY_DETAILS_NAME: "Invalid value."}),
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )
    except ports_exceptions.TemplateDoesNotExist:
        logger.warning("Template '%s' does not exist.", template_id)
        return make_response(
            jsonify({consts.ERROR_RESPONSE_KEY_DETAILS_NAME: "Template not found."}),
            HTTPStatus.NOT_FOUND,
        )

    return make_response(jsonify({"message": "Template value set."}), HTTPStatus.OK)
