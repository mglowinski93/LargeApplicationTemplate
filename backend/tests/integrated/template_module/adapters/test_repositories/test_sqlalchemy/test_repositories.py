import pytest
from typing import Callable

from sqlalchemy.orm import Session

from modules.template_module.adapters.repositories.sqlalchemy.consts import (
    VALUE_NAME_IN_DATABASE,
)
from modules.template_module.adapters.repositories.sqlalchemy.orm import (
    Template as TemplateDb,
)
from modules.template_module.adapters.repositories.sqlalchemy import (
    SqlAlchemyTemplatesDomainRepository,
    SqlAlchemyTemplatesQueryRepository,
)
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.ports.dtos import TemplatesFilters
from modules.template_module.domain.ports import exceptions
from ...... import fakers
from ......unit import factories as entity_factories


def test_domain_repository_creates_template(db_session: Session):
    # Given
    template_entity = entity_factories.TemplateEntityFactory.create()
    repository = SqlAlchemyTemplatesDomainRepository(db_session)

    # When
    repository.create(template_entity)
    db_session.commit()

    # Then
    result = db_session.query(TemplateDb).filter_by(id=template_entity.id).one()
    assert result.id == template_entity.id


def test_domain_repository_updates_template(
    db_session: Session, persistent_template_entity_factory: Callable
):
    # Given
    template_entity = persistent_template_entity_factory(
        value=fakers.fake_template_value()
    )
    repository = SqlAlchemyTemplatesDomainRepository(db_session)
    new_template_value = fakers.fake_template_value()

    # When
    template_entity.set_value(value=new_template_value)
    repository.update(template_entity)
    db_session.commit()

    # Then
    result = (
        db_session.query(TemplateDb).filter_by(id=template_entity.id).one()
    )  # Exactly one result must be present in a database. Otherwise, error is raised.
    db_session.refresh(result)
    assert result.value_data[VALUE_NAME_IN_DATABASE] == new_template_value.value


def test_domain_repository_deletes_template(
    db_session: Session, persistent_template_entity_factory: Callable
):
    # Given
    template_entity = persistent_template_entity_factory(
        value=fakers.fake_template_value()
    )
    repository = SqlAlchemyTemplatesDomainRepository(db_session)

    # When
    repository.delete(template_entity.id)
    db_session.commit()

    # Then
    result = db_session.query(TemplateDb).filter_by(id=template_entity.id).one_or_none()
    assert result is None


def test_domain_repository_can_retrieve_template(
    db_session: Session, persistent_template_entity_factory: Callable
):
    # Given
    template_entity = persistent_template_entity_factory()
    repository = SqlAlchemyTemplatesDomainRepository(db_session)

    # When
    result = repository.get(template_entity.id)

    # Then
    assert isinstance(result, TemplateEntity)
    assert result == template_entity


def test_query_repository_can_retrieve_template(
    db_session_factory: Callable, persistent_template_entity_factory: Callable
):
    # Given
    template_entity = persistent_template_entity_factory()
    repository = SqlAlchemyTemplatesQueryRepository(db_session_factory)

    # When
    result = repository.get(template_entity.id)

    # Then
    assert isinstance(result, TemplateEntity)
    assert result == template_entity


def test_query_repository_raises_exception_when_template_does_not_exist(
    db_session_factory: Callable,
):
    # Given
    repository = SqlAlchemyTemplatesQueryRepository(db_session_factory)

    # When
    with pytest.raises(exceptions.TemplateDoesNotExist):
        repository.get(template_id=fakers.fake_template_id())


def test_query_repository_lists_templates(
    db_session_factory: Callable, persistent_template_entity_factory: Callable
):
    # Given
    number_of_templates = 3
    template_entities = [
        persistent_template_entity_factory() for _ in range(number_of_templates)
    ]
    repository = SqlAlchemyTemplatesQueryRepository(db_session_factory)

    # When
    results, total_number_of_results = repository.list(
        filters=TemplatesFilters(),
        ordering=[],
        pagination=None,
    )

    # Then
    assert isinstance(results, list)
    assert all(isinstance(result, TemplateEntity) for result in results)
    assert set(results) == set(template_entities)
    assert total_number_of_results == number_of_templates
