import inspect
import sys
from typing import List, Type

import factory

from modules.common import time
from modules.common.database.orm import Base
from modules.template_module.adapters.repositories.sqlalchemy.consts import (
    VALUE_NAME_IN_DATABASE,
)
from modules.template_module.adapters.repositories.sqlalchemy.orm import (
    Template as SqlAlchemyTemplateDb,
)
from modules.template_module.domain.value_objects import (
    INITIAL_TEMPLATE_VERSION,
)

from .fakers import fake_template_id, fake_template_value


class AbstractSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model: Base | None = None
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"


class TemplateFactory(AbstractSQLAlchemyModelFactory):
    class Meta:
        model = SqlAlchemyTemplateDb

    id = factory.LazyFunction(fake_template_id)
    value_data = factory.LazyFunction(
        lambda: {VALUE_NAME_IN_DATABASE: fake_template_value().value}
    )
    timestamp = factory.LazyFunction(time.get_current_timestamp)
    version = INITIAL_TEMPLATE_VERSION


def get_model_factories() -> List[Type[AbstractSQLAlchemyModelFactory]]:
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    subclasses = [
        cls
        for _, cls in classes
        if issubclass(cls, AbstractSQLAlchemyModelFactory)
        and cls is not AbstractSQLAlchemyModelFactory
    ]
    return subclasses
