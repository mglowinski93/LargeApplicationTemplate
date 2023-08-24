from uuid import UUID
from http import HTTPStatus

from flask import abort, request

from . import api_blueprint
from ...domain import exceptions as domain_exceptions, value_objects
from ...domain.ports import exceptions as ports_exceptions
from ...services import template_service, unit_of_work


@api_blueprint.route("/<template_id>", methods=["POST"])
def set_template_id(template_id: str):
    """
    file: ./swagger_files/delete_stored_backup_endpoint.yml
    """

    try:
        template_id: value_objects.TEMPLATE_ID_TYPE = UUID(template_id)  # type: ignore
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, {"message": "Invalid template id format."})

    try:
        template_service.set_template_value(
            unit_of_work=unit_of_work.SqlAlchemyTemplateUnitOfWork(),
            template_id=template_id,  # type: ignore
            value=value_objects.TemplateValue(value=request.get_json()["value"]),
        )
    except domain_exceptions.InvalidTemplateValue:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, {"message": "Invalid value."})
    except ports_exceptions.TemplateDoesNotExist:
        abort(HTTPStatus.NOT_FOUND)
    except KeyError:
        abort(HTTPStatus.BAD_REQUEST, {"message": "Missing value field."})

    return {"message": "Template value set."}, HTTPStatus.OK
