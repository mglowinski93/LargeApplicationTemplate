from uuid import UUID
from http import HTTPStatus

from flask import abort, jsonify, make_response, request

from . import api_blueprint
from ... import services
from ...domain import exceptions as domain_exceptions, value_objects
from ...domain.ports import exceptions as ports_exceptions


@api_blueprint.route("/<template_id>", methods=["GET"])
def get_template_endpoint(template_id: str):
    """
    file: ../../../../swagger_files/template_endpoints/get_template.yml
    """

    try:
        template_id: value_objects.TEMPLATE_ID_TYPE = UUID(template_id)  # type: ignore
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, {"message": "Invalid template ID format."})

    try:
        template = services.get_template(
            unit_of_work=services.SqlAlchemyTemplateUnitOfWork(),
            template_id=template_id,  # type: ignore
        )
    except ports_exceptions.TemplateDoesNotExist:
        abort(HTTPStatus.NOT_FOUND)

    return make_response(jsonify(template.serialize()), HTTPStatus.OK)


@api_blueprint.route("/", methods=["GET"])
def list_templates_endpoint():
    """
    file: ../../../../swagger_files/template_endpoints/list_templates.yml
    """

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

    template = services.create_template(
        unit_of_work=services.SqlAlchemyTemplateUnitOfWork(),
    )

    return make_response(jsonify(template), HTTPStatus.CREATED)


@api_blueprint.route("/<template_id>", methods=["PATCH"])
def set_template_value_endpoint(template_id: str):
    """
    file: ../../../../swagger_files/template_endpoints/set_template_value.yml
    """

    try:
        template_id: value_objects.TEMPLATE_ID_TYPE = UUID(template_id)  # type: ignore
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, {"message": "Invalid template ID format."})

    try:
        services.set_template_value(
            unit_of_work=services.SqlAlchemyTemplateUnitOfWork(),
            template_id=template_id,  # type: ignore
            value=value_objects.TemplateValue(value=request.get_json()["value"]),
        )
    except domain_exceptions.InvalidTemplateValue:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, {"message": "Invalid value."})
    except ports_exceptions.TemplateDoesNotExist:
        abort(HTTPStatus.NOT_FOUND)
    except KeyError:
        abort(HTTPStatus.BAD_REQUEST, {"message": "Missing value field."})

    return make_response(jsonify({"message": "Template value set."}), HTTPStatus.OK)
