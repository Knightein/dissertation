import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, NoneOf


class RegisterForm(FlaskForm):
    # Fields
    email = EmailField(validators=[Email(), DataRequired("Please enter your email address.")])

    firstname = StringField(validators=[NoneOf(['*', '?', '!', "'", '^', '+', '%', '&', '/',
                                                '(', ')', '=', '}', ']', '[', '{', '$', '#', '@', '<', '>']),
                                        DataRequired("Please enter your first name.")])

    lastname = StringField(validators=[NoneOf(['*', '?', '!', "'", '^', '+', '%', '&', '/',
                                               '(', ')', '=', '}', ']', '[', '{', '$', '#', '@', '<', '>']),
                                       DataRequired("Please enter your last name.")])

    password = PasswordField(validators=[
        Length(min=6, max=15, message="Password must be between 6 and 15 characters long."),
        DataRequired("Please enter a password.")
    ])

    confirm_password = PasswordField(validators=[
        EqualTo('password', message='Passwords must match.'),
        DataRequired("Please confirm your password.")
    ])

    submit = SubmitField()

    # Custom validators
    def validate_password(self, password):
        # Must contain any digit, any A-Z character, any a-z character, and any special character
        regex = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-+?_=,<>/])')
        # Check if password matches regex -- if not, raise ValidationError
        if not regex.match(password.data):
            raise ValidationError('Password must contain at least one digit, one uppercase letter, one lowercase '
                                  'letter, and one special character.')


class LoginForm(FlaskForm):
    email = StringField(validators=[Email(), DataRequired("Please enter your email address.")])
    password = PasswordField(validators=[DataRequired("Please enter a password.")])
    submit = SubmitField()
