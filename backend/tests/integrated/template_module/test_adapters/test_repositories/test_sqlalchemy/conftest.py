from typing import Callable, Optional

import pytest
from sqlalchemy.orm import Session

from modules.template_module.adapters.repositories.sqlalchemy.consts import (
    VALUE_NAME_IN_DATABASE,
)
from modules.template_module.adapters.repositories.sqlalchemy.repository import (
    _map_template_db_to_template_entity,
)
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.value_objects import TemplateValue
from .factories import TemplateSqlAlchemyModelFactory



