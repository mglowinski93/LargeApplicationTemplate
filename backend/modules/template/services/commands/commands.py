from modules.common.message_bus import MessageBus
from modules.common.time import get_current_timestamp

from ...domain import commands as domain_commands
from ...domain import entities
from ...domain import events as domain_events
from ...domain.ports.unit_of_work import AbstractTemplatesUnitOfWork
from ...domain.value_objects import INITIAL_TEMPLATE_VERSION
from ..queries.dtos import OutputTemplate
from ..queries.mappers import map_template_entity_to_output_dto

# In this example app, there is no need to care much about history of changes,
# and rather focus on separating business logic from infrastructure and data integrity.

# In case there is a need to track history of changes,
# adapts the following approach:
# https://www.cosmicpython.com/book/part2.html.

# Allocate here invokes of business logic related to particular action,
# transaction management, and data transformations.
# In other words,
# allocate here bridge logic between the presentation and data access layers,
# or any other
# that doesn't belong neither to the domain layer nor to the infrastructure layer.

# In this approach, a service layer is responsible for generating events.
# More details can be found here:
# https://www.cosmicpython.com/book/chapter_08_events_and_message_bus.html.


def create_template(
    templates_unit_of_work: AbstractTemplatesUnitOfWork,
    message_bus: MessageBus,
    command: domain_commands.CreateTemplate,
) -> (
    OutputTemplate
):  # It's correct to return data from command when no data are queried.
    # This approach meets the CQS pattern rules.
    # More details can be found here:
    # https://martinfowler.com/bliki/CommandQuerySeparation.html.

    template = entities.Template(
        id=entities.Template.generate_id(),
        timestamp=get_current_timestamp(),
        version=INITIAL_TEMPLATE_VERSION,
    )
    output = map_template_entity_to_output_dto(template)

    with templates_unit_of_work:
        templates_unit_of_work.templates.create(template)

    message_bus.handle(
        [
            domain_events.TemplateCreated(
                template_id=template.id, timestamp=template.timestamp
            )
        ]
    )

    return output


def delete_template(
    templates_unit_of_work: AbstractTemplatesUnitOfWork,
    message_bus: MessageBus,
    command: domain_commands.DeleteTemplate,
) -> None:
    with templates_unit_of_work:
        templates_unit_of_work.templates.delete(command.template_id)

    message_bus.handle([domain_events.TemplateDeleted(template_id=command.template_id)])


def set_template_value(
    templates_unit_of_work: AbstractTemplatesUnitOfWork,
    message_bus: MessageBus,
    command: domain_commands.SetTemplateValue,
) -> None:
    with templates_unit_of_work:
        template = templates_unit_of_work.templates.get(command.template_id)
        template.set_value(command.value)
        templates_unit_of_work.templates.update(template)

    message_bus.handle(
        [domain_events.TemplateValueSet(template_id=template.id, value=command.value)],
    )


def subtract_template_value(
    templates_unit_of_work: AbstractTemplatesUnitOfWork,
    message_bus: MessageBus,
    command: domain_commands.SubtractTemplateValue,
) -> None:
    with templates_unit_of_work:
        template: entities.Template = templates_unit_of_work.templates.get(
            command.template_id
        )
        final_value = template.subtract_value(command.value)
        templates_unit_of_work.templates.update(template)

    message_bus.handle(
        [
            domain_events.TemplateValueSubtracted(
                template_id=template.id,
                subtracted_value=command.value,
                final_value=final_value,
            )
        ]
    )
