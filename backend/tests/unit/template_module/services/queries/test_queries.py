from typing import Callable

import pytest

from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.ports.exceptions import TemplateDoesNotExist
from modules.template_module.services import get_template, list_templates
from ... import factories
from ..... import fakers as common_fakers

def test_get_template_returns_output_dto_when_template_exists(
    fake_template_query_repository_factory: Callable,
):
    # Given
    template = factories.TemplateEntityFactory.create()
    query_repository = fake_template_query_repository_factory(
        initial_templates=[template]
    )

    # When
    output_template_dto = get_template(
        query_repository=query_repository,
        template_id=template.id,
    )

    # Then
    assert output_template_dto == map_template_entity_to_output_detailed_dto(
        template
    )


def test_get_template_raises_exception_when_requested_template_doesnt_exist(
    fake_template_query_repository_factory: Callable,
):
    with pytest.raises(TemplateDoesNotExist):
        get_template(
            query_repository=fake_template_query_repository_factory(
                initial_templates=[]
            ),
            template_id=common_fakers.fake_template_id(),
        )


def test_list_templates_lists_all_templates(
    fake_template_query_repository_factory: Callable,
):
    # Given
    templates = [factories.TemplateEntityFactory.create()]
    query_repository = fake_template_query_repository_factory(
        initial_templates=templates
    )

    # When
    results, total_number_of_results = list_templates(
        query_repository=query_repository,
    )

    # Then
    assert results == [
        map_template_entity_to_output_dto(template) for template in templates
    ]


def test_list_templates_returns_empty_list_when_no_templates_exist(
    fake_template_query_repository_factory: Callable,
):
    # Given
    query_repository = fake_template_query_repository_factory(initial_templates=[])

    # When
    results, total_number_of_results = list_templates(
        query_repository=query_repository,
    )

    # Then
    assert isinstance(results, list)
    assert not results
    assert total_number_of_results == 0
