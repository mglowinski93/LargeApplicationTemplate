from abc import ABC, abstractmethod

from ..domain.models import Template
from ..domain.value_objects import TEMPLATE_ID_TYPE


class TemplateRepository(ABC):
    @abstractmethod
    def save(self, template: Template):
        pass

    @abstractmethod
    def get(self, template_id: TEMPLATE_ID_TYPE) -> Template:
        pass

    @abstractmethod
    def list(self) -> list[Template]:
        pass
