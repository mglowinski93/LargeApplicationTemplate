from abc import ABC, abstractmethod

from .....common.dtos import Ordering
from .....common.pagination.dtos import Pagination
from .....template_module.domain.entities import Template
from .....template_module.domain.ports.dtos import TemplatesFilters
from .....template_module.domain.value_objects import TemplateId


class AbstractTemplatesQueryRepository(ABC):
    @abstractmethod
    def get(self, template_id: TemplateId) -> Template:
        """
        :param template_id: ID of template to retrieve.
        :raises TemplateDoesNotExist: Template with given id doesn't exist.

        :return: Template with given id.
        """

        pass

    @abstractmethod
    def list(
        self,
        filters: TemplatesFilters,
        ordering: list[Ordering | None],
        pagination: Pagination | None = None,
    ) -> tuple[list[Template], int]:
        """
        :param filters: Filters to apply.
        :param ordering: Ordering to apply.
        :param pagination: Pagination to apply.
        :return: List of all templates and
                 total count of templates matching given filters.
        """

        pass
