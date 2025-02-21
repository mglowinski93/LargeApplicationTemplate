from collections import deque
from typing import Optional, List, Sequence

from faker import Faker

from modules.common.dtos import Ordering, OrderingEnum
from modules.common.message_bus import MessageBus, Message
from modules.common.pagination import Pagination
from modules.common.domain.events import Event as DomainEvent
from modules.common.domain.commands import Command as DomainCommand
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.ports.dtos import TemplatesFilters
from modules.template_module.domain.value_objects import TEMPLATE_ID_TYPE
from modules.template_module.domain.ports import (
    AbstractTemplateDomainRepository,
    exceptions,
)
from modules.template_module.domain.ports.unit_of_work import (
    AbstractTemplatesUnitOfWork,
)
from modules.template_module.services.queries.ports import (
    AbstractTemplateQueryRepository,
)
from modules.template_module.domain.events.template import TemplateValueSet


from tests.factories import FakeTaskDispatcher


fake = Faker()


class FakeTemplateRepository(AbstractTemplateDomainRepository):
    def __init__(self, templates: list[TemplateEntity]):
        self._templates = set(templates)

    def create(self, template: TemplateEntity):
        # Template entities can be compared, due ot that hash method is implemented.
        if template in self._templates:
            self._templates.remove(template)
        self._templates.add(template)

    def delete(self, template_id: TEMPLATE_ID_TYPE):
        self._templates.remove(self.get(template_id=template_id))

    def get(self, template_id: TEMPLATE_ID_TYPE) -> TemplateEntity:
        try:
            return next(
                template for template in self._templates if template.id == template_id
            )
        except StopIteration as err:
            raise exceptions.TemplateDoesNotExist(
                f"Template with id '{template_id}' doesn't exist."
            ) from err

    def update(self, template: TemplateEntity):
        self._templates.remove(self.get(template_id=template.id))
        self._templates.add(template)


class FakeTemplateQueryRepository(AbstractTemplateQueryRepository):
    def __init__(self, templates: list[TemplateEntity]):
        self._templates = set(templates)

    def get(self, template_id: TEMPLATE_ID_TYPE) -> TemplateEntity:
        try:
            return next(
                template for template in self._templates if template.id == template_id
            )
        except StopIteration as err:
            raise exceptions.TemplateDoesNotExist(
                f"Template with id '{template_id}' doesn't exist."
            ) from err

    def list(
        self,
        filters: TemplatesFilters,
        ordering: list[Ordering],
        pagination: Optional[Pagination] = None,
    ) -> tuple[list[TemplateEntity], int]:
        templates = self._filter(templates=self._templates, filters=filters)
        templates = self._order(templates=templates, ordering=ordering)

        if pagination is not None:
            templates = self._paginate(templates=templates, pagination=pagination)

        return list(templates), len(templates)

    @staticmethod
    def _filter(
        templates: set[TemplateEntity],
        filters: TemplatesFilters,
    ) -> set[TemplateEntity]:
        if filters.value is not None:
            templates = {t for t in templates if t.value == filters.value}

        if filters.query is not None:
            templates = {
                template
                for template in templates
                if str(template.id).lower().find(filters.query.lower()) != -1
            }

        if filters.timestamp_from is not None:
            templates = {
                template
                for template in templates
                if template.timestamp >= filters.timestamp_from
            }

        if filters.timestamp_to is not None:
            templates = {
                template
                for template in templates
                if template.timestamp <= filters.timestamp_to
            }

        return templates

    @staticmethod
    def _order(
        templates: set[TemplateEntity], ordering: List[Ordering]
    ) -> set[TemplateEntity]:
        for order in ordering:
            if order.field == "timestamp":
                sorted(
                    templates,
                    key=lambda template: (template.value is None, template.value),
                    reverse=(order.order == OrderingEnum.DESCENDING),
                )
            elif order.field == "value":
                sorted(
                    templates,
                    key=lambda template: (template.value is None, template.value),
                    reverse=(order.order == OrderingEnum.DESCENDING),
                )

        return templates

    @staticmethod
    def _paginate(
        templates: set[TemplateEntity], pagination: Pagination
    ) -> set[TemplateEntity]:
        start = pagination.offset
        return set(list(templates)[start : start + pagination.records_per_page])


class FakeTemplateUnitOfWork(AbstractTemplatesUnitOfWork):
    def __init__(self, templates: list[TemplateEntity]):
        self.templates = FakeTemplateRepository(templates=templates)
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakeMessageBus(MessageBus):
    def __init__(self, fake_task_dispatcher: FakeTaskDispatcher):
        self.queue: deque[Message] = deque()
        self.fake_task_dispatcher = fake_task_dispatcher

    def handle(self, messages: Sequence[Message]):
        self.queue.extend(messages)

        while self.queue:
            message = self.queue.popleft()

            if isinstance(message, DomainEvent):
                self.handle_event(message)
            elif isinstance(message, DomainCommand):
                self.handle_command(message)

    def handle_event(self, event: DomainEvent):
        if isinstance(event, TemplateValueSet):
            self.fake_task_dispatcher.send_email("test")
        else:
            pass

    def handle_command(self, command: DomainCommand):
        pass
