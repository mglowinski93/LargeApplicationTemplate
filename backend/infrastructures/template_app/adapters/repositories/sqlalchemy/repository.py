from apps.template_app.ports import TemplateRepository
from apps.template_app.domain.models import Template
from apps.template_app.domain.value_objects import TEMPLATE_ID_TYPE


class SqlAlchemyTemplateRepository(TemplateRepository):
    def __init__(self, session):
        self.session = session

    def add(self, template: Template):
        self.session.add(template)

    def get(self, template_id: TEMPLATE_ID_TYPE):
        return self.session.query(Template).filter_by(id=template_id).one()

    def list(self):
        return self.session.query(Template).all()
