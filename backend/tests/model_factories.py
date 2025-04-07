import inspect
import sys
from functools import partial
from typing import Any, List, Type

import factory

from modules.common import time
from modules.common.database.orm import Base
from modules.template.adapters.repositories.sqlalchemy.consts import (
    VALUE_NAME_IN_DATABASE,
)
from modules.template.adapters.repositories.sqlalchemy.orm import (
    Template as SqlAlchemyTemplateDb,
)
from modules.template.domain.value_objects import (
    INITIAL_TEMPLATE_VERSION,
)

from .fakers import fake_template_id, fake_template_value


class GenerateDataMixin:
    @classmethod
    def generate_data(cls):
        def convert_dict_from_stub(
            stub: factory.base.StubObject, factory_: factory.Factory
        ) -> dict[str, Any]:
            stub_dict = stub.__dict__

            for key, value in stub_dict.items():
                if isinstance(value, factory.base.StubObject):
                    if key in factory_._meta.declarations and isinstance(
                        factory_._meta.declarations[key], factory.Factory
                    ):
                        factory_ = factory_._meta.declarations[key]

                    stub_dict[key] = convert_dict_from_stub(value, factory_)
                    continue

                if (
                    key
                    in [field.name for field in factory_._meta.model._meta.get_fields()]
                    and factory_._meta.model._meta.get_field(key).choices
                ):
                    stub_dict[key] = next(
                        (
                            _value
                            for _key, _value in factory_._meta.model._meta.get_field(
                                key
                            ).choices
                            if value == _key
                        ),
                        value,
                    )
                    continue

            return stub_dict

        def dict_factory(factory, **kwargs):
            return convert_dict_from_stub(factory.stub(**kwargs), factory)

        return partial(dict_factory, cls)()


class AbstractSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model: Base | None = None
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"


class TemplateFactory(GenerateDataMixin, AbstractSQLAlchemyModelFactory):
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
    return [
        cls
        for _, cls in classes
        if issubclass(cls, AbstractSQLAlchemyModelFactory)
        and cls is not AbstractSQLAlchemyModelFactory
    ]
