from abc import ABC, abstractmethod
from typing import Optional

from .dtos import TemplatesFilters
from ..entities import Template
from ..value_objects import TEMPLATE_ID_TYPE
from ....common.dtos import Ordering
from ....common.pagination import Pagination


class AbstractTemplateDomainRepository(ABC):
    @abstractmethod
    def save(self, template: Template):
        """
        :param template: Template to save.
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

    #TODO list method to be deleted. Remember to unhook in all places and possibly switch with QueryRepository.

    @abstractmethod
    def list(
        self,
        filters: TemplatesFilters,
        ordering: list[Ordering],
        pagination: Optional[Pagination] = None,
    ) -> tuple[list[Template], int]:
        """
        :return: List of all templates and
                 total count of templates matching given filters.
        """

        pass
