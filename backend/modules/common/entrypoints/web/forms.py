from wtforms import Form, StringField, validators

from ...dtos import Ordering, OrderingEnum


class OrderingForm(Form):
    ordering = StringField(validators=[validators.DataRequired()])

    def create_ordering(self) -> list[Ordering] | None:
        order: list[Ordering] = [
            self._get_ordering_for_single_field(field)
            for field in self.ordering.data.split(",")
            if any(key in field for key in ("timestamp",))
        ]
        return order if order else None

    def _get_ordering_for_single_field(self, field: str) -> Ordering:
        if field.startswith("-"):
            return Ordering(field=field[1:].strip(), order=OrderingEnum.DESCENDING)
        return Ordering(field=field.strip(), order=OrderingEnum.ASCENDING)
