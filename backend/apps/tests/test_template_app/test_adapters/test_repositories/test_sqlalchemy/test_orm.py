from typing import Callable

from sqlalchemy.orm import Session

from apps.template_app.domain.entities import Template as TemplateEntity


def test_template_mapper_can_load_templates(
    db_session: Session, template_sqlalchemy_factory: Callable
):
    # Given
    template_entity = template_sqlalchemy_factory()

    # When
    result = db_session.query(TemplateEntity).filter_by(id=template_entity.id).one()

    # Then
    assert isinstance(result, TemplateEntity)
    assert result == template_entity


def test_template_mapper_can_save_templates(
    db_session: Session, template_entity: TemplateEntity
):
    # When
    db_session.add(template_entity)
    db_session.commit()

    # Then
    rows = db_session.query(TemplateEntity).all()
    assert len(rows) == 1
    assert rows[0] == template_entity
    assert isinstance(rows[0], TemplateEntity)
