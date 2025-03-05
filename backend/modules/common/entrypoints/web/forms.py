from wtforms import Form, StringField, validators

from ...dtos import Ordering, OrderingEnum


class OrderingForm(Form):
    ordering = StringField(validators=[validators.DataRequired()])

    def create_ordering(self) -> list[Ordering | None] | None:
        order: list[Ordering | None] = [
            self._get_ordering_for_single_field(field)
            for field in self.ordering.data.split(",")
        ]

        if order[0] is None:
            return None

        return order

    def _get_ordering_for_single_field(self, field: str) -> Ordering | None:
        if field.strip() == "":
            return None

        if field.startswith("-"):
            return Ordering(field=field[1:], order=OrderingEnum.DESCENDING)
        return Ordering(field=field, order=OrderingEnum.ASCENDING)
