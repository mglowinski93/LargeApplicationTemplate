from typing import Callable

import pytest

from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.ports.exceptions import TemplateDoesNotExist
from modules.template_module.services import get_template, list_templates
from modules.template_module.services.mappers import map_template_entity_to_output_dto
from ....factories import fake_template_id


def test_get_template_returns_output_dto_when_template_exists(
    fake_template_unit_of_work_factory: Callable,
    template_entity: TemplateEntity,
):
    # Given
    unit_of_work = fake_template_unit_of_work_factory(
        initial_templates=[template_entity]
    )

    # When
    output_template_dto = get_template(
        unit_of_work=unit_of_work,
        template_id=template_entity.id,
    )

    # Then
    assert output_template_dto == map_template_entity_to_output_dto(template_entity)


def test_get_template_raises_exception_when_requested_template_doesnt_exist(
    fake_template_unit_of_work_factory: Callable,
):
    with pytest.raises(TemplateDoesNotExist):
        get_template(
            unit_of_work=fake_template_unit_of_work_factory(initial_templates=[]),
            template_id=fake_template_id(),
        )


def test_list_templates_lists_all_templates(
    fake_template_unit_of_work_factory: Callable,
    template_entity: TemplateEntity,
):
    # Given
    templates = [template_entity]
    unit_of_work = fake_template_unit_of_work_factory(initial_templates=templates)

    # When
    results, total_number_of_results = list_templates(
        unit_of_work=unit_of_work,
    )

    # Then
    assert results == [
        map_template_entity_to_output_dto(template) for template in templates
    ]


def test_list_templates_returns_empty_list_when_no_templates_exist(
    fake_template_unit_of_work_factory: Callable,
    template_entity: TemplateEntity,
):
    # Given
    unit_of_work = fake_template_unit_of_work_factory(initial_templates=[])

    # When
    results, total_number_of_results = list_templates(
        unit_of_work=unit_of_work,
    )

    # Then
    assert isinstance(results, list)
    assert not results
    assert total_number_of_results == 0
