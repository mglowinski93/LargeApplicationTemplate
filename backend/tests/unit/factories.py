import factory

from modules.common import time
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.value_objects import (
    INITIAL_TEMPLATE_VERSION,
)


class TemplateEntityFactory(factory.Factory):
    class Meta:
        model = TemplateEntity

    id = factory.LazyFunction(TemplateEntity.generate_id)
    timestamp = factory.LazyFunction(time.get_current_utc_timestamp)
    version = INITIAL_TEMPLATE_VERSION
