import pytest

from ..test_adapters.test_repositories.test_sqlalchemy.conftest import (
    db_session,  # noqa: F401
    template_sqlalchemy_factory,  # noqa: F401
)


@pytest.fixture
def db_session_factory(db_session):  # noqa: F811
    def db_session_():
        return db_session

    return db_session_
