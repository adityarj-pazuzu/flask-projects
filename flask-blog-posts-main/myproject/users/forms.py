from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from myproject.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Email or Username is required')])
    password = PasswordField('Password', validators=[DataRequired(message='Password is required')])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):

    email = EmailField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password',
                                 validators=[DataRequired(), EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email ID already registered")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already exists")


class UpdateUserForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email ID already registered")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already exists")
