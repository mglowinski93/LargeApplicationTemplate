from abc import ABC, abstractmethod

from ..entities import Template
from ..value_objects import TEMPLATE_ID_TYPE


class TemplateRepository(ABC):
    @abstractmethod
    def save(self, template: Template):
        """
        :param template: Template to save.
        :return:
        """

        pass

    @abstractmethod
    def get(self, template_id: TEMPLATE_ID_TYPE) -> Template:
        """
        :raises TemplateDoesNotExist: Template with given id doesn't exist.
        :param template_id: ID of template to get.
        :return: Template with given id.
        """

        pass

    @abstractmethod
    def list(self) -> list[Template]:
        """
        :return: List of all templates.
        """

        pass
