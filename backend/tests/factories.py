from uuid import UUID, uuid4

import factory
from faker import Faker

from modules.common.time import get_current_utc_timestamp
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.value_objects import TemplateValue

fake = Faker()


class TemplateEntityFactory(factory.Factory):
    class Meta:
        model = TemplateEntity

    id = factory.LazyFunction(uuid4)
    timestamp = factory.LazyFunction(get_current_utc_timestamp)


def fake_template_id() -> UUID:
    return uuid4()


def fake_template_value() -> TemplateValue:
    return TemplateValue(value=fake.pystr(min_chars=1, max_chars=100))
