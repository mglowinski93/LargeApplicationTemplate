from ..queries.dtos import OutputTemplate
from ..queries.mappers import map_template_entity_to_output_dto
from ...domain.events import (
    TemplateValueSet,
    TemplateCreated,
    TemplateDeleted,
)
from ...domain.commands import (
    SetTemplateValue,
    CreateTemplate,
    DeleteTemplate,
)
from ....common.message_bus import MessageBus
from ....common.time import get_current_utc_timestamp
from ...domain import entities
from ...domain.ports.unit_of_work import AbstractTemplatesUnitOfWork
from ...domain.value_objects import INITIAL_TEMPLATE_VERSION


# In this example app, there is no need to care much about history of changes,
# and rather focus on separating business logic from infrastructure and data integrity.

# In case there is a need to track history of changes,
# adapts the following approach:
# https://www.cosmicpython.com/book/part2.html.


def create_template(
    templates_unit_of_work: AbstractTemplatesUnitOfWork,
    message_bus: MessageBus,
    command: CreateTemplate,
) -> (
    OutputTemplate
):  # It's correct to return data from command when no data are queried.
    # This approach meets the CQS pattern rules.
    # More details can be found here:
    # https://martinfowler.com/bliki/CommandQuerySeparation.html.

    template = entities.Template(
        id=entities.Template.generate_id(),
        timestamp=get_current_utc_timestamp(),
        version=INITIAL_TEMPLATE_VERSION,
    )
    output = map_template_entity_to_output_dto(template)

    with templates_unit_of_work:
        templates_unit_of_work.templates.create(template)
        message_bus.handle(
            messages=(
                TemplateCreated(template_id=template.id, timestamp=template.timestamp),
            )
        )

    return output


def delete_template(
    templates_unit_of_work: AbstractTemplatesUnitOfWork,
    message_bus: MessageBus,
    command: DeleteTemplate,
):
    with templates_unit_of_work:
        templates_unit_of_work.templates.delete(command.template_id)
        message_bus.handle(
            messages=[
                TemplateDeleted(template_id=command.template_id),
            ]
        )


def set_template_value(
    templates_unit_of_work: AbstractTemplatesUnitOfWork,
    message_bus: MessageBus,
    command: SetTemplateValue,
):
    """
    Allocate here invokes of business logic related to particular action,
    transaction management, and data transformations.

    In other words,
    allocate here bridge logic between the presentation and data access layers,
    or any other
    that doesn't belong neither to the domain layer nor to the infrastructure layer.
    """

    with templates_unit_of_work:
        template = templates_unit_of_work.templates.get(command.template_id)
        entities.set_template_value(template=template, value=command.value)
        templates_unit_of_work.templates.create(template)

        # In this approach, a service layer is responsible for generating events.
        # More details can be found here:
        # https://www.cosmicpython.com/book/chapter_08_events_and_message_bus.html.
        message_bus.handle(
            messages=[
                TemplateValueSet(template_id=template.id, value=command.value),
            ]
        )
