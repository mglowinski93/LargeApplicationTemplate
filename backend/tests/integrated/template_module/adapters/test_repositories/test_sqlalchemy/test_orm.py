import warnings

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from modules.common.time import get_current_utc_timestamp
from modules.template_module.adapters.repositories.sqlalchemy.orm import (
    Template as TemplateDb,
)
from modules.template_module.domain.value_objects import INITIAL_TEMPLATE_VERSION
from ...... import fakers


def test_orm_creates_default_value_for_template_model_value_data_field(
    db_session: Session,
):
    # Given
    template_instance = TemplateDb(
        id=fakers.fake_template_id(),
        timestamp=get_current_utc_timestamp(),
        version=INITIAL_TEMPLATE_VERSION,
    )
    db_session.add(template_instance)
    db_session.flush()

    # When
    result = db_session.query(TemplateDb).filter_by(id=template_instance.id).one()

    # Then
    assert isinstance(result, TemplateDb)
    assert isinstance(result.value_data, dict)


@pytest.mark.parametrize(
    "missing_field, set_fields",
    [
        (
            "id",
            {
                "timestamp": "get_current_utc_timestamp()",
                "version": "INITIAL_TEMPLATE_VERSION",
            },
        ),
        (
            "timestamp",
            {"id": "fakers.fake_template_id()", "version": "INITIAL_TEMPLATE_VERSION"},
        ),
        (
            "version",
            {"id": "fakers.apfake_template_id()", "timestamp": "get_current_utc_timestamp()"},
        ),
    ],
)
def test_orm_doesnt_have_default_value_for_missing_fields(
    db_session: Session, missing_field: str, set_fields: dict
):
    with pytest.raises(IntegrityError):
        with warnings.catch_warnings():
            # Temporary ignore the warning about missing value for the specified field.
            warnings.simplefilter("ignore")

            db_session.add(
                TemplateDb(**{key: eval(value) for key, value in set_fields.items()})
            )

            db_session.commit()
