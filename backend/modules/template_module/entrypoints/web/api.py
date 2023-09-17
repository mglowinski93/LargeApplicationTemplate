import logging
from uuid import UUID
from http import HTTPStatus

import inject
from flask import jsonify, make_response, request
from werkzeug.datastructures import MultiDict

from . import api_blueprint
from . import forms as template_forms
from ... import services
from ...domain import exceptions as domain_exceptions, value_objects
from ...domain.ports import exceptions as ports_exceptions, dtos as ports_dtos
from ...domain.ports.unit_of_work import UnitOfWork
from ....common import pagination as pagination_utils, consts
from ....common.entrypoints.web import forms as common_forms


logger = logging.getLogger(__name__)


@api_blueprint.route("/<template_id>", methods=["GET"])
@inject.params(unit_of_work="main_unit_of_work")
def get_template_endpoint(template_id: str, unit_of_work: UnitOfWork):
    """
    file: ../../../../swagger_files/template_endpoints/get_template.yml
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
            unit_of_work=unit_of_work,
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
@inject.params(unit_of_work="main_unit_of_work")
def list_templates_endpoint(unit_of_work: UnitOfWork):
    """
    file: ../../../../swagger_files/template_endpoints/list_templates.yml
    """

    logger.debug("Listing all templates.")

    query_params = request.args
    logger.debug("Query params are: '%s'.", query_params)

    try:
        pagination = pagination_utils.Pagination(
            offset=query_params.get(consts.PAGINATION_OFFSET_QUERY_PARAMETER_NAME, 0),
            records_per_page=query_params.get(
                consts.PAGINATION_LIMIT_QUERY_PARAMETER_NAME, 10
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

    ordering = (
        common_forms.OrderingForm(
            data=request.args,
            meta={"csrf": False},
        ).create_ordering()
        if consts.ORDERING_QUERY_PARAMETER_NAME in query_params
        else None
    )

    templates, all_templates_count = services.list_templates(
        unit_of_work=unit_of_work,
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
@inject.params(unit_of_work="main_unit_of_work")
def create_template_endpoint(unit_of_work: UnitOfWork):
    """
    file: ../../../../swagger_files/template_endpoints/create_template.yml
    """

    logger.info("Creating a new template.")

    template = services.create_template(
        unit_of_work=unit_of_work,
    )
    logger.info("Template '%s' created.", template.id)

    return make_response(jsonify(template.serialize()), HTTPStatus.CREATED)


@api_blueprint.route("/<template_id>", methods=["DELETE"])
@inject.params(unit_of_work="main_unit_of_work")
def delete_template_endpoint(template_id: str, unit_of_work: UnitOfWork):
    """
    file: ../../../../swagger_files/template_endpoints/delete_template.yml
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
        services.delete_template(
            unit_of_work=unit_of_work,
            template_id=template_id,  # type: ignore
        )
        logger.debug("Template '%s' found.", template_id)
    except ports_exceptions.TemplateDoesNotExist:
        logger.warning("Template '%s' does not exist.", template_id)
        return make_response(
            jsonify({consts.ERROR_RESPONSE_KEY_DETAILS_NAME: "Template not found."}),
            HTTPStatus.NOT_FOUND,
        )

    return make_response("", HTTPStatus.NO_CONTENT)


@api_blueprint.route("/<template_id>", methods=["PATCH"])
@inject.params(unit_of_work="main_unit_of_work")
def set_template_value_endpoint(template_id: str, unit_of_work: UnitOfWork):
    """
    file: ../../../../swagger_files/template_endpoints/set_template_value.yml
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
        services.set_template_value(
            unit_of_work=unit_of_work,
            template_id=template_id,  # type: ignore
            value=value_objects.TemplateValue(value=template_value),
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
