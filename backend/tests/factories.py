import factory
from sqlalchemy.orm import Session

from modules.common import time
from modules.template_module.adapters.repositories.sqlalchemy.consts import (
    VALUE_NAME_IN_DATABASE,
)
from modules.template_module.adapters.repositories.sqlalchemy.orm import (
    Template as SqlAlchemyTemplateDb,
)
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.value_objects import (
    INITIAL_TEMPLATE_VERSION,
)

from .fakers import fake_template_id, fake_template_value


def TemplateEntityFactory(
    session: Session | None = None, persistence: str | None = None
):
    class _TemplatePersistentEntityFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = SqlAlchemyTemplateDb
            sqlalchemy_session = session
            sqlalchemy_session_persistence = persistence

        id = factory.LazyFunction(fake_template_id)
        value_data = factory.LazyFunction(
            lambda: {VALUE_NAME_IN_DATABASE: fake_template_value().value}
        )
        timestamp = factory.LazyFunction(time.get_current_timestamp)
        version = INITIAL_TEMPLATE_VERSION

    class _TemplateEntityFactory(factory.Factory):
        class Meta:
            model = TemplateEntity

        id = factory.LazyFunction(fake_template_id)
        timestamp = factory.LazyFunction(time.get_current_timestamp)
        version = INITIAL_TEMPLATE_VERSION

    return _TemplatePersistentEntityFactory if session else _TemplateEntityFactory
