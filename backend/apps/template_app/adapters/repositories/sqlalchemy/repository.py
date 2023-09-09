from sqlalchemy.exc import NoResultFound

from ....domain.ports import TemplateRepository, exceptions
from ....domain.entities import Template as TemplateEntity
from ....domain.value_objects import TEMPLATE_ID_TYPE


class SqlAlchemyTemplateRepository(TemplateRepository):
    """
    See description of parent class to get more details.
    """

    def __init__(self, session):
        self.session = session

    def save(self, template: TemplateEntity):
        self.session.add(template)

    def get(self, template_id: TEMPLATE_ID_TYPE) -> TemplateEntity:
        try:
            return self.session.query(TemplateEntity).filter_by(id=template_id).one()
        except NoResultFound as err:
            raise exceptions.TemplateDoesNotExist(
                f"Template with id '{template_id}' doesn't exist."
            ) from err

    def list(self) -> list[TemplateEntity]:
        return self.session.query(TemplateEntity).all()
