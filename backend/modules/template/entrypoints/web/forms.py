from wtforms import DateTimeField, Form, IntegerField, StringField, validators

strip_filter = lambda x: x.strip() if x else None  # noqa: E731


class TemplatesFiltersForm(Form):
    query = StringField(filters=[strip_filter])
    timestamp_from = DateTimeField()
    timestamp_to = DateTimeField()


class SetTemplateValueForm(Form):
    value = IntegerField(validators=[validators.DataRequired()])


class SubtractTemplateValueForm(Form):
    value = IntegerField(validators=[validators.DataRequired()])
