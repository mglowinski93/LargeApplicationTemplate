from typing import Callable

from sqlalchemy.orm import Session

from apps.template_app.domain.entities import Template as TemplateEntity
from apps.template_app.domain.value_objects import TemplateValue
from ......factories import fake_template_value


def test_template_mapper_can_load_templates(
    db_session: Session, template_sqlalchemy_factory: Callable
):
    # Given
    template_entity = template_sqlalchemy_factory(value=fake_template_value())

    # When
    result = db_session.query(TemplateEntity).filter_by(id=template_entity.id).one()

    # Then
    assert isinstance(result, TemplateEntity)
    assert isinstance(result.value, TemplateValue)
    assert result == template_entity


def test_template_mapper_can_save_templates(
    db_session: Session, template_entity: TemplateEntity
):
    # Given
    template_entity.set_value(value=fake_template_value())

    # When
    db_session.add(template_entity)
    db_session.commit()

    # Then
    rows = db_session.query(TemplateEntity).all()
    assert len(rows) == 1
    record = rows[0]
    assert isinstance(record, TemplateEntity)
    assert isinstance(record.value, TemplateValue)
    assert record == template_entity
