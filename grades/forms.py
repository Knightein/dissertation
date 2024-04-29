import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.fields.simple import TextAreaField, BooleanField
from wtforms.validators import DataRequired


class GradeForm(FlaskForm):
    # Fields
    grade = StringField(validators=[DataRequired("Please enter the grade of the assignment.")])
    feedback = TextAreaField(validators=[DataRequired("Please enter a the feedback of the assignment.")])
    next_steps = TextAreaField(validators=[DataRequired("Please enter the next steps of the assignment.")])
    correct = BooleanField()
    code_submission = TextAreaField(validators=[DataRequired("Please enter the code submission of the assignment.")])
    submit = SubmitField()

    # Custom validators
    def validate_grade(self, grade):
        # Check for valid grade format
        regex = re.compile(r'^[A-FU]$')
        # If date does not match regex, raise ValidationError
        if not regex.match(grade.data):
            raise ValidationError("Grade must be A, B, C, D, F, or U.")
