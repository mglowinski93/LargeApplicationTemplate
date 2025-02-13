from datetime import datetime
from typing import Optional

from sqlalchemy import String, or_, text
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, Query
from sqlalchemy_utils.functions import cast_if

from .consts import VALUE_NAME_IN_DATABASE
from .orm import Template as TemplateDb
from ....domain.ports import (
    AbstractTemplateDomainRepository,
    exceptions,
    dtos as ports_dtos,
)
from ....domain.entities import Template as TemplateEntity
from ....domain.value_objects import TEMPLATE_ID_TYPE, TemplateValue
from .....common.dtos import Ordering, OrderingEnum
from .....common.pagination import Pagination
from .....template_module.services.queries.ports.repository import (
    AbstractTemplateQueryRepository,
)


class SqlAlchemyTemplateDomainRepository(AbstractTemplateDomainRepository):
    """
    See description of parent class to get more details.
    """

    def __init__(self, session):
        self.session = session

    def create(self, template: TemplateEntity) -> None:
        template_instance = (
            self.session.query(TemplateDb).filter_by(id=template.id).one_or_none()
        )
        if template_instance is None:
            self.session.add(_map_template_entity_to_template_db(template))
            return
        
    def update(self, template: TemplateEntity) -> None:
        try:
            template_instance = (
                self.session.query(TemplateDb).filter_by(id=template.id).scalar_one()
            )
        except NoResultFound as err:
            raise exceptions.TemplateDoesNotExist(
                f"Cannot update template with id '{template.id}', because it doesn't exist."
            ) from err
        
        for key, value in _map_template_entity_to_template_db(
            template
        ).__dict__.items():
            if key != "_sa_instance_state":
                setattr(template_instance, key, value)       

    def delete(self, template_id: TEMPLATE_ID_TYPE):
        try:
            self.session.delete(
                self.session.query(TemplateDb).filter_by(id=template_id).one()
            )
        except NoResultFound as err:
            raise exceptions.TemplateDoesNotExist(
                f"Template with id '{template_id}' doesn't exist."
            ) from err

    def get(self, template_id: TEMPLATE_ID_TYPE) -> TemplateEntity:
        try:
            return _map_template_db_to_template_entity(
                self.session.query(TemplateDb)
                .filter_by(id=template_id)
                .with_for_update()
                .one()
            )
        except NoResultFound as err:
            raise exceptions.TemplateDoesNotExist(
                f"Template with id '{template_id}' doesn't exist."
            ) from err


class SqlAlchemyTemplateQueryRepository(AbstractTemplateQueryRepository):
    def __init__(self, session):
        self.session = session

    def get(self, template_id: TEMPLATE_ID_TYPE) -> TemplateEntity:
        try:
            return _map_template_db_to_template_entity(
                self.session.query(TemplateDb).filter_by(id=template_id).one()
            )
        except NoResultFound as err:
            raise exceptions.TemplateDoesNotExist(
                f"Template with id '{template_id}' doesn't exist."
            ) from err

    def list(
        self,
        filters: ports_dtos.TemplatesFilters,
        ordering: list[Ordering],
        pagination: Optional[Pagination] = None,
    ) -> tuple[list[TemplateEntity], int]:
        templates, query = _get_templates(
            filters=filters,
            ordering=ordering,
            pagination=pagination,
            session=self.session,
        )
        return templates, query.count()


def _get_templates(
    session: Session,
    filters: ports_dtos.TemplatesFilters,
    ordering: list[Ordering],
    pagination: Optional[Pagination] = None,
) -> tuple:
    query = session.query(TemplateDb)

    query = _filter(query=query, filters=filters)

    for order in ordering:
        query = _order(query=query, order=order)

    not_paginated_query = query

    if pagination is not None:
        query = _paginate(query=query, pagination=pagination)

    return (
        [_map_template_db_to_template_entity(template) for template in query.all()],
        not_paginated_query,
    )


def _filter(query: Query, filters: ports_dtos.TemplatesFilters):
    if filters.value is not None:
        query = query.filter(
            text("value_data->>'value' = :val").params(val=filters.value)
        )

    if filters.query is not None:
        query = query.filter(
            or_(
                cast_if(TemplateDb.id, String).ilike(f"%{filters.query}%"),
                # Add here other fields that should be searchable.
                # Example:
                #    TemplateDb.value_data.ilike(f"%{filters.query}%"),
            )
        )

    query = _filter_timestamp(
        query=query,
        timestamp_from=filters.timestamp_from,
        timestamp_to=filters.timestamp_to,
    )

    return query


def _filter_timestamp(
    query: Query, timestamp_from: Optional[datetime], timestamp_to: Optional[datetime]
):
    if timestamp_from is not None:
        query = query.where(TemplateDb.timestamp >= timestamp_from)

    if timestamp_to is not None:
        query = query.where(TemplateDb.timestamp <= timestamp_to)

    return query


def _order(query: Query, order: Ordering):
    if order.order == OrderingEnum.ASCENDING:
        return _asc_order(query, order.field)

    return _desc_order(query, order.field)


def _asc_order(query, field: str):
    if field == "timestamp":
        return query.order_by(TemplateDb.timestamp.asc())

    if field == "value":
        return query.order_by(text(f"value_data->>'{VALUE_NAME_IN_DATABASE}' ASC"))


def _desc_order(query: Query, field: str):
    if field == "timestamp":
        return query.order_by(TemplateDb.timestamp.desc())

    if field == "value":
        return query.order_by(text(f"value_data->>'{VALUE_NAME_IN_DATABASE}' DESC"))


def _paginate(query: Query, pagination: Pagination):
    return query.limit(pagination.records_per_page).offset(pagination.offset)


def _map_template_entity_to_template_db(
    template_entity: TemplateEntity,
) -> TemplateDb:
    return TemplateDb(
        id=template_entity.id,
        value_data=_map_template_value_dto_to_dict(template_entity.value),
        timestamp=template_entity.timestamp,
        version=template_entity.version,
    )


def _map_template_db_to_template_entity(
    template_db: TemplateDb,
) -> TemplateEntity:
    entity = TemplateEntity(
        id=template_db.id,
        timestamp=template_db.timestamp,
        version=template_db.version,
    )
    # The Assumption is that data in a database are always correct and
    # can be safely loaded to an entity.
    entity._value = _map_template_data_dict_to_dto(template_db.value_data)
    return entity


def _map_template_value_dto_to_dict(template_value: TemplateValue) -> dict:
    return {
        VALUE_NAME_IN_DATABASE: template_value.value
        if template_value.value is not None
        else None,
    }


def _map_template_data_dict_to_dto(template_dict: dict) -> TemplateValue:
    return TemplateValue(value=template_dict.get(VALUE_NAME_IN_DATABASE))
