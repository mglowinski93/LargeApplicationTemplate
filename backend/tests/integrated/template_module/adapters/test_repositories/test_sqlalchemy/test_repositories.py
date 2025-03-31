from datetime import timezone
from typing import Callable

import pytest
from dateutil import tz
from sqlalchemy.orm import Session

from modules.common.time import TIME_ZONE
from modules.template_module.adapters.repositories.sqlalchemy import (
    SqlAlchemyTemplatesDomainRepository,
    SqlAlchemyTemplatesQueryRepository,
)
from modules.template_module.adapters.repositories.sqlalchemy.consts import (
    VALUE_NAME_IN_DATABASE,
)
from modules.template_module.adapters.repositories.sqlalchemy.orm import (
    Template as TemplateDb,
)
from modules.template_module.adapters.repositories.sqlalchemy.repositories import (
    _map_template_db_to_template_entity,
)
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.ports import exceptions
from modules.template_module.domain.ports.dtos import TemplatesFilters

from ...... import entity_factories, fakers, model_factories


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
    timestamp = result.timestamp
    assert timestamp.tzinfo is not None
    assert timestamp.tzinfo == timezone.utc


def test_domain_repository_updates_template(
    db_session: Session,
):
    # Given
    repository = SqlAlchemyTemplatesDomainRepository(db_session)
    template_entity = _map_template_db_to_template_entity(
        model_factories.TemplateFactory.create()
    )

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
    db_session: Session,
):
    # Given
    repository = SqlAlchemyTemplatesDomainRepository(db_session)
    template_entity = _map_template_db_to_template_entity(
        model_factories.TemplateFactory.create()
    )

    # When
    repository.delete(template_entity.id)
    db_session.commit()

    # Then
    result = db_session.query(TemplateDb).filter_by(id=template_entity.id).one_or_none()
    assert result is None


def test_domain_repository_can_retrieve_template(
    db_session: Session,
):
    # Given
    repository = SqlAlchemyTemplatesDomainRepository(db_session)
    template_entity = _map_template_db_to_template_entity(
        model_factories.TemplateFactory.create()
    )

    # When
    result = repository.get(template_entity.id)
    # Then
    assert isinstance(result, TemplateEntity)
    assert result == template_entity
    assert result.timestamp.tzinfo == tz.gettz(TIME_ZONE)


def test_query_repository_can_retrieve_template(
    db_session_factory: Callable,
):
    # Given
    template_entity = _map_template_db_to_template_entity(
        model_factories.TemplateFactory.create()
    )

    query_repository = SqlAlchemyTemplatesQueryRepository(db_session_factory)

    # When
    result = query_repository.get(template_entity.id)

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
    db_session_factory: Callable,
):
    # Given
    number_of_templates = 3
    template_entites = [
        _map_template_db_to_template_entity(template)
        for template in model_factories.TemplateFactory.create_batch(
            number_of_templates
        )
    ]
    query_repository = SqlAlchemyTemplatesQueryRepository(db_session_factory)

    # When
    results, total_number_of_results = query_repository.list(
        filters=TemplatesFilters(),
        ordering=[],
        pagination=None,
    )

    # Then
    assert isinstance(results, list)
    assert all(isinstance(result, TemplateEntity) for result in results)
    assert set(results) == set(template_entites)
    assert total_number_of_results == number_of_templates
