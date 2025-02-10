from abc import ABC, abstractmethod
from typing import Optional

from ....services.dtos import OutputTemplate, DetailedOutputTemplate
from .....common.dtos import Ordering
from .....common.pagination.dtos import Pagination
from .....template_module.domain.value_objects import TEMPLATE_ID_TYPE
from .....template_module.domain.ports.dtos import TemplatesFilters


class AbstractTemplatesQueryRepository(ABC):
    @abstractmethod
    def get(self, template_id: TEMPLATE_ID_TYPE) -> DetailedOutputTemplate:
        """
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
    ) -> tuple[list[OutputTemplate], int]:
        """
        :return: List of all templates and
                 total count of templates matching given filters.
        """

        pass
