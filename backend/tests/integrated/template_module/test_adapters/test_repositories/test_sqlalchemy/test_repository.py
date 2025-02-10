from typing import Callable

from sqlalchemy.orm import Session

from modules.template_module.adapters.repositories.sqlalchemy.consts import (
    VALUE_NAME_IN_DATABASE,
)
from modules.template_module.adapters.repositories.sqlalchemy.orm import (
    Template as TemplateDb,
)
from modules.template_module.adapters.repositories.sqlalchemy import (
    SqlAlchemyTemplateDomainRepository,
)
from modules.template_module.domain.entities import Template as TemplateEntity
from modules.template_module.domain.ports.dtos import TemplatesFilters
from ......factories import fake_template_value


def test_repository_creates_template(
    db_session: Session, template_entity: TemplateEntity
):
    # Given
    repository = SqlAlchemyTemplateDomainRepository(db_session)

    # When
    repository.save(template_entity)
    db_session.commit()

    # Then
    result = db_session.query(TemplateDb).filter_by(id=template_entity.id).one()
    assert result.id == template_entity.id


def test_repository_updates_template(
    db_session: Session, persistent_template_entity_factory: Callable
):
    # Given
    template_entity = persistent_template_entity_factory(value=fake_template_value())
    repository = SqlAlchemyTemplateDomainRepository(db_session)
    new_template_value = fake_template_value()

    # When
    template_entity.set_value(value=new_template_value)
    repository.save(template_entity)
    db_session.commit()

    # Then
    result = (
        db_session.query(TemplateDb).filter_by(id=template_entity.id).one()
    )  # Exactly one result must be present in a database. Otherwise, error is raised.
    db_session.refresh(result)
    assert result.value_data[VALUE_NAME_IN_DATABASE] == new_template_value.value


def test_repository_deletes_template(
    db_session: Session, persistent_template_entity_factory: Callable
):
    # Given
    template_entity = persistent_template_entity_factory(value=fake_template_value())
    repository = SqlAlchemyTemplateDomainRepository(db_session)

    # When
    repository.delete(template_entity.id)
    db_session.commit()

    # Then
    result = db_session.query(TemplateDb).filter_by(id=template_entity.id).one_or_none()
    assert result is None


def test_repository_can_retrieve_template(
    db_session: Session, persistent_template_entity_factory: Callable
):
    # Given
    template_entity = persistent_template_entity_factory()
    repository = SqlAlchemyTemplateDomainRepository(db_session)

    # When
    result = repository.get(template_entity.id)

    # Then
    assert isinstance(result, TemplateEntity)
    assert result == template_entity


def test_repository_lists_templates(
    db_session: Session, persistent_template_entity_factory: Callable
):
    # Given
    number_of_templates = 3
    template_entities = [
        persistent_template_entity_factory() for _ in range(number_of_templates)
    ]
    repository = SqlAlchemyTemplateDomainRepository(db_session)

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
