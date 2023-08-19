from sqlalchemy.orm import Session

from apps.template_app.adapters.repositories.sqlalchemy import (
    SqlAlchemyTemplateRepository,
)
from apps.template_app.adapters.repositories.sqlalchemy.database import (
    Template as TemplateSqlAlchemyModel,
)


def test_repository_can_save_template(
    db_session: Session, template_sqlalchemy_model: TemplateSqlAlchemyModel
):
    # Given
    repository = SqlAlchemyTemplateRepository(db_session)

    # When
    repository.save(template_sqlalchemy_model)
    db_session.commit()

    # Then
    rows = db_session.query(
        TemplateSqlAlchemyModel.id,
        TemplateSqlAlchemyModel.value,
        TemplateSqlAlchemyModel.timestamp,
    ).all()
    assert len(rows) == 1
    assert list(rows) == template_sqlalchemy_model


def test_repository_can_retrieve_template(
    db_session: Session, template_sqlalchemy_model: TemplateSqlAlchemyModel
):
    # Given
    repository = SqlAlchemyTemplateRepository(db_session)

    # When
    retrieved_template = repository.get(template_sqlalchemy_model.id)

    # Then
    assert retrieved_template == template_sqlalchemy_model


def test_repository_can_list_templates(
    db_session: Session, template_sqlalchemy_model: TemplateSqlAlchemyModel
):
    # Given
    repository = SqlAlchemyTemplateRepository(db_session)

    # When
    retrieved_template = repository.list(template_sqlalchemy_model.id)[0]

    # Then
    assert retrieved_template == template_sqlalchemy_model
