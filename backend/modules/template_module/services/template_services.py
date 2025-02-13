from .dtos import OutputTemplate
from ..domain.events.template import TemplateValueSet
from .mappers import map_template_entity_to_output_dto
from .template_message_bus import handle_event
from ..domain import entities, value_objects
from ..domain.ports.unit_of_work import AbstractTemplatesUnitOfWork
from ..domain.value_objects import INITIAL_TEMPLATE_VERSION
from ...common.time import get_current_utc_timestamp


# In this example app, there is no need to care much about history of changes,
# and rather focus on separating business logic from infrastructure and data integrity.

# In case there is a need to track history of changes,
# adapts the following approach:
# https://www.cosmicpython.com/book/part2.html.


def create_template(
    unit_of_work: AbstractTemplatesUnitOfWork,
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

    with unit_of_work:
        unit_of_work.templates.create(template)

    return output


def delete_template(
    unit_of_work: AbstractTemplatesUnitOfWork,
    template_id: value_objects.TEMPLATE_ID_TYPE,
):
    with unit_of_work:
        unit_of_work.templates.delete(template_id)


def set_template_value(
    unit_of_work: AbstractTemplatesUnitOfWork,
    template_id: value_objects.TEMPLATE_ID_TYPE,
    value: value_objects.TemplateValue,
):
    """
    Allocate here invokes of business logic related to particular action,
    transaction management, and data transformations.

    In other words,
    allocate here bridge logic between the presentation and data access layers,
    or any other
    that doesn't belong neither to the domain layer nor to the infrastructure layer.
    """

    with unit_of_work:
        template = unit_of_work.templates.get(template_id)
        entities.set_template_value(template=template, value=value)
        unit_of_work.templates.create(template)

        # In this approach, a service layer is responsible for generating events.
        # More details can be found here:
        # https://www.cosmicpython.com/book/chapter_08_events_and_message_bus.html.
        # Moreover, in this example we don't care much about
        handle_event(TemplateValueSet(template_id=template.id, value=value))
