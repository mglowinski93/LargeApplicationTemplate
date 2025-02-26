from abc import ABC, abstractmethod
from typing import Optional

from .....common.dtos import Ordering
from .....common.pagination.dtos import Pagination
from .....template_module.domain.value_objects import TemplateId
from .....template_module.domain.ports.dtos import TemplatesFilters
from .....template_module.domain.entities import Template


class AbstractTemplatesQueryRepository(ABC):
    @abstractmethod
    def get(self, template_id: TemplateId) -> Template:
        """
        :raises TemplateDoesNotExist: Template with given id doesn't exist.
        :param template_id: ID of template to retrieve.
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
