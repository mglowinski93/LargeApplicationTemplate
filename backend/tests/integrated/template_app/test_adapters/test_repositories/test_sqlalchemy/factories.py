from uuid import uuid4

import factory

from apps.common.time import get_current_utc_timestamp
from apps.template_app.adapters.repositories.sqlalchemy.consts import (
    VALUE_NAME_IN_DATABASE,
)
from apps.template_app.adapters.repositories.sqlalchemy.orm import (
    Template as SqlAlchemyTemplateDb,
)


class TemplateSqlAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SqlAlchemyTemplateDb

    id = factory.LazyFunction(uuid4)
    value_data = factory.LazyFunction(lambda: {VALUE_NAME_IN_DATABASE: None})
    timestamp = factory.LazyFunction(get_current_utc_timestamp)
