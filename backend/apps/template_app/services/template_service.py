from ..domain import entities


def set_template_value(template: entities.Template, value: entities.TemplateValue):
    """
    Allocate here invokes of business logic related to particular action,
    transaction management, and data transformations.

    In other words,
    allocate here bridge logic between the presentation and data access layers,
    or any other
    that doesn't belong neither to the domain layer nor to the infrastructure layer.
    """

    entities.set_template_value(template=template, value=value)
