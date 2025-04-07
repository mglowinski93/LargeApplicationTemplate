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
        :param template: Template to update.
        :raises TemplateDoesNotExist: Template with given id doesn't exist.
        :return:
        """

        pass

    @abstractmethod
    def delete(self, template_id: TemplateId):
        """
        :param template_id: ID of template to delete.
        :raises TemplateDoesNotExist: Template with given id doesn't exist.

        :return:
        """

        pass

    @abstractmethod
    def get(self, template_id: TemplateId) -> Template:
        """
        :param template_id: ID of template to retrieve.
        :raises TemplateDoesNotExist: Template with given id doesn't exist.

        :return: Template with given id.
        """

        pass
