from abc import ABC, abstractmethod
from typing import Optional

from .dtos import TemplatesFilters
from ..entities import Template
from ..value_objects import TEMPLATE_ID_TYPE
from ....common.dtos import Ordering
from ....common.pagination import Pagination


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
