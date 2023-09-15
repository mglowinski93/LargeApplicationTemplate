import warnings

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from modules.common.time import get_current_utc_timestamp
from modules.template_module.adapters.repositories.sqlalchemy.orm import (
    Template as TemplateDb,
)
from ......factories import fake_template_id


def test_orm_creates_default_value_for_template_model_value_data_field(
    db_session: Session,
):
    # Given
    template_instance = TemplateDb(
        id=fake_template_id(),
        timestamp=get_current_utc_timestamp(),
    )
    db_session.add(template_instance)
    db_session.flush()

    # When
    result = db_session.query(TemplateDb).filter_by(id=template_instance.id).one()

    # Then
    assert isinstance(result, TemplateDb)
    assert isinstance(result.value_data, dict)


def test_orm_doesnt_have_default_value_for_template_model_id(db_session: Session):
    with pytest.raises(IntegrityError):
        with warnings.catch_warnings():
            # Temporary ignore the warning about missing value for the primary key.
            warnings.simplefilter("ignore")
            db_session.add(
                TemplateDb(
                    timestamp=get_current_utc_timestamp(),
                )
            )
            db_session.commit()
