from abc import ABC, abstractmethod

from ..entities import Template
from ..value_objects import TemplateId


class AbstractTemplatesDomainRepository(ABC):
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
    def delete(self, template_id: TemplateId):
        """
        :raises TemplateDoesNotExist: Template with given id doesn't exist.
        :param template_id: ID of template to delete.
        :return:
        """

        pass

    @abstractmethod
    def get(self, template_id: TemplateId) -> Template:
        """
        :raises TemplateDoesNotExist: Template with given id doesn't exist.
        :param template_id: ID of template to retrieve.
        :return: Template with given id.
        """

        pass
