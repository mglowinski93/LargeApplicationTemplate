from abc import ABC, abstractmethod

from ..entities import Template
from ..value_objects import TEMPLATE_ID_TYPE


class AbstractTemplateDomainRepository(ABC):
    @abstractmethod
    def create(self, template: Template):
        """
        :param template: Template to save.
        :return:
        """

        pass

    @abstractmethod
    def update(self, template: Template):
        """
        :raises TemplateDoesNotExist: Template with given id doesn't exist.
        :param template: Template to update.
        :return:
        """

        pass

    @abstractmethod
    def delete(self, template_id: TEMPLATE_ID_TYPE):
        """
        :raises TemplateDoesNotExist: Template with given id doesn't exist.
        :param template_id: ID of template to delete.
        :return:
        """

        pass

    @abstractmethod
    def get(self, template_id: TEMPLATE_ID_TYPE) -> Template:
        """
        :raises TemplateDoesNotExist: Template with given id doesn't exist.
        :param template_id: ID of template to retrieve.
        :return: Template with given id.
        """

        pass
