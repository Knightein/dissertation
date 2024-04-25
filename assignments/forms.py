import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired


class AssignmentForm(FlaskForm):
    # Fields
    assignment_name = StringField(validators=[DataRequired("Please enter the name of the assignment.")])
    description = TextAreaField(validators=[DataRequired("Please enter a description of the assignment.")])
    due_date = StringField(validators=[DataRequired("Please enter the due date of the assignment.")])
    submit = SubmitField()

    # Custom validators
    def validate_due_date(self, due_date):
        # Check for valid date format
        regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        # If date does not match regex, raise ValidationError
        if not regex.match(due_date.data):
            raise ValidationError("Due date must be in the format YYYY-MM-DD.")
