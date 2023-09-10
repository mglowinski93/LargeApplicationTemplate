from wtforms import Form, StringField


strip_filter = lambda x: x.strip() if x else None  # noqa: E731


class SetTemplateValueForm(Form):
    value = StringField(filters=[strip_filter])
