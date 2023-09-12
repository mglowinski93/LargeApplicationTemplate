from datetime import datetime
from typing import Optional

from sqlalchemy import String, asc, desc, or_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, Query
from sqlalchemy_utils.functions import cast_if

from ....domain.ports import TemplateRepository, exceptions, dtos as ports_dtos
from ....domain.entities import Template as TemplateEntity
from ....domain.value_objects import TEMPLATE_ID_TYPE
from .....common.dtos import Ordering, OrderingEnum
from .....common.pagination import Pagination


class SqlAlchemyTemplateRepository(TemplateRepository):
    """
    See description of parent class to get more details.
    """

    def __init__(self, session):
        self.session = session

    def save(self, template: TemplateEntity):
        self.session.add(template)

    def get(self, template_id: TEMPLATE_ID_TYPE) -> TemplateEntity:
        try:
            return self.session.query(TemplateEntity).filter_by(id=template_id).one()
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
    query = session.query(TemplateEntity)

    query = _filter(query=query, filters=filters)

    for order in ordering:
        query = _order(query=query, order=order)

    not_paginated_query = query

    if pagination is not None:
        query = _paginate(query=query, pagination=pagination)

    return (
        query.all(),
        not_paginated_query,
    )


def _filter(query: Query, filters: ports_dtos.TemplatesFilters):
    if filters.value is not None:
        query = query.filter_by(value_data=filters.value)

    if filters.query is not None:
        query = query.filter(
            or_(
                cast_if(TemplateEntity.id, String).ilike(f"%{filters.query}%"),
                # Add here other fields that should be searchable.
                # Example:
                #    TemplateEntity.value_data.ilike(f"%{filters.query}%"),
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
        query = query.where(TemplateEntity.timestamp >= timestamp_from)  # type: ignore

    if timestamp_to is not None:
        query = query.where(TemplateEntity.timestamp <= timestamp_to)  # type: ignore

    return query


def _order(query: Query, order: Ordering):
    if order.order == OrderingEnum.ASCENDING:
        return _asc_order(query, order.field)

    return _desc_order(query, order.field)


def _asc_order(query, field: str):
    if field == "timestamp":
        return query.order_by(TemplateEntity.timestamp.asc())  # type: ignore

    if field == "value":
        return query.order_by(asc(TemplateEntity._value))  # type: ignore


def _desc_order(query: Query, field: str):
    if field == "timestamp":
        return query.order_by(TemplateEntity.timestamp.desc())  # type: ignore

    if field == "value":
        return query.order_by(desc(TemplateEntity._value))  # type: ignore


def _paginate(query: Query, pagination: Pagination):
    return query.limit(pagination.records_per_page).offset(pagination.offset)
