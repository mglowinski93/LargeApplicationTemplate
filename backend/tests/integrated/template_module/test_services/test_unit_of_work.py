from typing import Callable

import pytest

from modules.template_module.adapters.repositories.sqlalchemy.orm import (
    Template as TemplateDb,
)
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.services.unit_of_work import SqlAlchemyTemplateUnitOfWork


def test_unit_of_work_can_retrieve_template(
    db_session_factory: Callable,
    persistent_template_entity_factory: Callable,
):
    # Given
    template_entity = persistent_template_entity_factory()
    unit_of_work = SqlAlchemyTemplateUnitOfWork(db_session_factory)

    # When
    with unit_of_work:
        received_template = unit_of_work.templates.get(template_entity.id)

    # Then
    assert isinstance(received_template, TemplateEntity)
    assert received_template == template_entity


def test_unit_of_work_can_save_template(
    db_session_factory: Callable,
    template_entity: TemplateEntity,
):
    # Given
    template_id = template_entity.id
    unit_of_work = SqlAlchemyTemplateUnitOfWork(db_session_factory)

    # When
    with unit_of_work:
        unit_of_work.templates.save(template_entity)

    # Then
    assert db_session_factory().get(TemplateDb, template_id)


def test_unit_of_work_rollbacks_when_exception_occur(
    db_session_factory: Callable,
    template_entity: TemplateEntity,
):
    # Given
    unit_of_work = SqlAlchemyTemplateUnitOfWork(db_session_factory)

    # When
    with pytest.raises(Exception):
        with unit_of_work:
            unit_of_work.templates.save(template_entity)
            raise Exception

    # Then
    assert db_session_factory().query(TemplateDb).count() == 0
