from ....domain.ports import TemplateRepository
from ....domain.entities import Template
from ....domain.value_objects import TEMPLATE_ID_TYPE


class SqlAlchemyTemplateRepository(TemplateRepository):
    def __init__(self, session):
        self.session = session

    def save(self, template: Template):
        self.session.add(template)

    def get(self, template_id: TEMPLATE_ID_TYPE):
        return self.session.query(Template).filter_by(id=template_id).one()

    def list(self):
        return self.session.query(Template).all()
