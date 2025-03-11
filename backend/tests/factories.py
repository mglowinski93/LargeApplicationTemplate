import factory
from sqlalchemy.orm import Session

from modules.common.time import get_current_utc_timestamp
from modules.template_module.adapters.repositories.sqlalchemy.orm import (
    Template as SqlAlchemyTemplateDb,
)
from modules.template_module.domain.value_objects import INITIAL_TEMPLATE_VERSION

from .fakers import fake_template_id, fake_template_value


class TemplateSqlAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SqlAlchemyTemplateDb
        sqlalchemy_session: Session | None = None

    id = factory.LazyFunction(fake_template_id)
    value_data = factory.LazyFunction(fake_template_value)
    timestamp = factory.LazyFunction(get_current_utc_timestamp)
    version = INITIAL_TEMPLATE_VERSION
