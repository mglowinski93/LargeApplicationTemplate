from ..domain import entities, value_objects
from ..domain.ports.unit_of_work import UnitOfWork


def set_template_value(
    unit_of_work: UnitOfWork,
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
        unit_of_work.templates.save(template)
