from wtforms import DateTimeField, Form, StringField, validators

strip_filter = lambda x: x.strip() if x else None  # noqa: E731


class TemplatesFiltersForm(Form):
    value = StringField(filters=[strip_filter])
    query = StringField(filters=[strip_filter])
    timestamp_from = DateTimeField()
    timestamp_to = DateTimeField()


class SetTemplateValueForm(Form):
    value = StringField(filters=[strip_filter], validators=[validators.DataRequired()])
