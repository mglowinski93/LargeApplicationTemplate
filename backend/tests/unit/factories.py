import factory

from modules.common import time
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.value_objects import (
    INITIAL_TEMPLATE_VERSION,
)

from ..fakers import fake_template_id


class TemplateEntityFactory(factory.Factory):
    class Meta:
        model = TemplateEntity

    id = factory.LazyFunction(fake_template_id)
    timestamp = factory.LazyFunction(time.get_current_utc_timestamp)
    version = INITIAL_TEMPLATE_VERSION
