import logging
from uuid import UUID
from http import HTTPStatus

from flask import abort, jsonify, make_response, request
from werkzeug.datastructures import MultiDict

from . import api_blueprint
from .forms import SetTemplateValueForm
from ... import services
from ...domain import exceptions as domain_exceptions, value_objects
from ...domain.ports import exceptions as ports_exceptions


logger = logging.getLogger(__name__)


@api_blueprint.route("/<template_id>", methods=["GET"])
def get_template_endpoint(template_id: str):
    """
    file: ../../../../swagger_files/template_endpoints/get_template.yml
    """

    logger.debug("Getting data for template '%s'.", template_id)

    try:
        template_id: value_objects.TEMPLATE_ID_TYPE = UUID(template_id)  # type: ignore
    except ValueError:
        logger.warning("Invalid template ID format: '%s'.", template_id)
        abort(HTTPStatus.BAD_REQUEST, {"message": "Invalid template ID format."})

    try:
        template = services.get_template(
            unit_of_work=services.SqlAlchemyTemplateUnitOfWork(),
            template_id=template_id,  # type: ignore
        )
        logger.debug("Template '%s' found.", template_id)
    except ports_exceptions.TemplateDoesNotExist:
        abort(HTTPStatus.NOT_FOUND)

    return make_response(jsonify(template.serialize()), HTTPStatus.OK)


@api_blueprint.route("/", methods=["GET"])
def list_templates_endpoint():
    """
    file: ../../../../swagger_files/template_endpoints/list_templates.yml
    """

    logger.debug("Listing all templates.")
    templates = services.list_templates(
        unit_of_work=services.SqlAlchemyTemplateUnitOfWork(),
    )

    return make_response(
        jsonify([template.serialize() for template in templates]), HTTPStatus.OK
    )


@api_blueprint.route("/", methods=["POST"])
def create_templates_endpoint():
    """
    file: ../../../../swagger_files/template_endpoints/create_template.yml
    """

    logger.info("Creating a new template.")

    template = services.create_template(
        unit_of_work=services.SqlAlchemyTemplateUnitOfWork(),
    )
    logger.info("Template '%s' created.", template.id)

    return make_response(jsonify(template), HTTPStatus.CREATED)


@api_blueprint.route("/<template_id>", methods=["PATCH"])
def set_template_value_endpoint(template_id: str):
    """
    file: ../../../../swagger_files/template_endpoints/set_template_value.yml
    """

    logger.info("Setting value for template '%s'.", template_id)

    try:
        template_id: value_objects.TEMPLATE_ID_TYPE = UUID(template_id)  # type: ignore
    except ValueError:
        logger.warning("Invalid template ID format: '%s'.", template_id)
        abort(HTTPStatus.BAD_REQUEST, {"message": "Invalid template ID format."})

    form = SetTemplateValueForm(
        formdata=MultiDict(request.get_json(force=True)),
        meta={"csrf": False},
    )
    if not form.validate():
        logger.warning("Request can't be handled, due to invalid input data.")
        return make_response(form.errors, HTTPStatus.BAD_REQUEST)

    template_value = form.data["value"]

    try:
        logger.info("Setting value for template '%s'.", template_id)
        services.set_template_value(
            unit_of_work=services.SqlAlchemyTemplateUnitOfWork(),
            template_id=template_id,  # type: ignore
            value=value_objects.TemplateValue(value=template_value),
        )
        logger.info("Value '%s' set for template '%s'.", template_value, template_id)
    except domain_exceptions.InvalidTemplateValue:
        logger.warning(
            "Invalid value '%s' for template '%s'.", template_value, template_id
        )
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, {"message": "Invalid value."})
    except ports_exceptions.TemplateDoesNotExist:
        logger.warning("Template '%s' does not exist.", template_id)
        abort(HTTPStatus.NOT_FOUND)

    return make_response(jsonify({"message": "Template value set."}), HTTPStatus.OK)
