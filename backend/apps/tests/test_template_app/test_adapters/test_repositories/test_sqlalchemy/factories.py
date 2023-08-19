from uuid import uuid4

import factory

from apps.common.time import get_current_utc_timestamp
from apps.template_app.adapters.repositories.sqlalchemy.database import (
    Template as SqlAlchemyTemplateModel,
)


class TemplateSqlAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SqlAlchemyTemplateModel

    id = factory.LazyFunction(uuid4)
    timestamp = factory.LazyFunction(get_current_utc_timestamp)
