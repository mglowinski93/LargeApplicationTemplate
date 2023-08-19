from typing import Callable

from sqlalchemy.orm import Session

from apps.template_app.adapters.repositories.sqlalchemy import (
    SqlAlchemyTemplateRepository,
)
from apps.template_app.domain.entities import Template as TemplateEntity


def test_repository_can_save_template(
    db_session: Session, template_entity: TemplateEntity
):
    # Given
    repository = SqlAlchemyTemplateRepository(db_session)

    # When
    repository.save(template_entity)
    db_session.commit()

    # Then
    result = db_session.query(TemplateEntity).filter_by(id=template_entity.id).one()
    assert result.id == template_entity.id


def test_repository_can_retrieve_template(
    db_session: Session, template_sqlalchemy_factory: Callable
):
    # Given
    template_entity = template_sqlalchemy_factory()
    repository = SqlAlchemyTemplateRepository(db_session)

    # When
    result = repository.get(template_entity.id)

    # Then
    assert isinstance(result, TemplateEntity)
    assert result == template_entity


def test_repository_can_list_templates(
    db_session: Session, template_sqlalchemy_factory: Callable
):
    # Given
    template_entity = template_sqlalchemy_factory()
    repository = SqlAlchemyTemplateRepository(db_session)

    # When
    result = repository.list()[0]

    # Then
    assert isinstance(result, TemplateEntity)
    assert result == template_entity
