from ..domain import models


def set_template_value(template: models.Template, value: models.TemplateValue):
    """
    Allocate here invokes of business logic related to particular action,
    transaction management, and data transformations.

    In other words,
    allocate here bridge logic between the presentation and data access layers,
    or any other
    that doesn't belong neither to the domain layer nor to the infrastructure layer.
    """

    models.set_template_value(template=template, value=value)
