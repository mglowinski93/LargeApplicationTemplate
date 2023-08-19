from ....domain.ports import TemplateRepository
from ....domain.entities import Template as TemplateEntity
from ....domain.value_objects import TEMPLATE_ID_TYPE


class SqlAlchemyTemplateRepository(TemplateRepository):
    def __init__(self, session):
        self.session = session

    def save(self, template: TemplateEntity):
        self.session.add(template)

    def get(self, template_id: TEMPLATE_ID_TYPE) -> TemplateEntity:
        return self.session.query(TemplateEntity).filter_by(id=template_id).one()

    def list(self) -> list[TemplateEntity]:
        return self.session.query(TemplateEntity).all()
