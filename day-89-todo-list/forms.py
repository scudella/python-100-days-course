from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class TodoForm(FlaskForm):
    title = StringField(
        "Task",
        validators=[
            DataRequired(message="Task cannot be empty."),
            Length(max=200, message="Task must be under 200 characters."),
        ],
        render_kw={"placeholder": "Add a new task..."},
    )
    submit = SubmitField("Add")


class ActionForm(FlaskForm):
    """Empty form used purely for CSRF protection on toggle/delete buttons."""
    pass
