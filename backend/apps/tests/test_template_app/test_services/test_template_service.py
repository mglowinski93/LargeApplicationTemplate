from typing import Callable

import pytest

from apps.template_app.domain.exceptions import InvalidTemplateValue
from apps.template_app.domain.entities import Template as TemplateEntity
from apps.template_app.domain.value_objects import TemplateValue
from apps.template_app.domain.ports.exceptions import TemplateDoesNotExist
from apps.template_app.services.template_service import set_template_value
from ..factories import fake_template_id, fake_template_value


def test_set_template_value_sets_value_when_valid_value(
    fake_repository_factory: Callable,
    template_entity: TemplateEntity,
):
    # Given
    value = fake_template_value()
    timestamp_before_setting_value = template_entity.timestamp
    repository = fake_repository_factory(initial_templates=[template_entity])

    # When
    set_template_value(
        repository=repository,
        template_id=template_entity.id,
        value=value,
    )

    # Then
    assert template_entity.value == value
    assert repository.get(template_entity.id).value == value
    assert timestamp_before_setting_value < template_entity.timestamp


def test_set_template_value_raises_exception_when_invalid_value(
    fake_repository_factory: Callable,
    template_entity: TemplateEntity,
):
    # Given
    value = TemplateValue(value="")
    timestamp_before_setting_value = template_entity.timestamp
    repository = fake_repository_factory(initial_templates=[template_entity])

    with pytest.raises(InvalidTemplateValue):
        set_template_value(
            repository=repository,
            template_id=template_entity.id,
            value=value,
        )

    assert timestamp_before_setting_value == template_entity.timestamp


def test_set_template_value_raises_exception_when_requested_template_doesnt_exist(
    fake_repository_factory: Callable,
):
    # Given
    value = fake_template_value()
    repository = fake_repository_factory(initial_templates=[])

    with pytest.raises(TemplateDoesNotExist):
        set_template_value(
            repository=repository,
            template_id=fake_template_id(),
            value=value,
        )

    assert not repository.list()
