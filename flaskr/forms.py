from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Regexp, Length


# Form for user login
class LoginForm(FlaskForm):
    username = StringField('username', validators=[
        InputRequired(message='Username is required'),
        Regexp(r"[A-Za-z0-9\-_\.]{4,20}")
    ])
    password = PasswordField('password', validators=[
        InputRequired(message='Password is required'),
        Regexp('[A-Za-z0-9_!@#$%^&*?]{7,20}')
    ])
    submit = SubmitField('Sign In')


# Form for user registration
class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[
        InputRequired(message='Username is required'),
        Regexp(r'[A-Za-z0-9_\-\.]{4,20}',
               message='Usernames can contain letters, numbers and select special characters'),
        Length(4, 20, message='Usernames must be between 4 and 20 character')
    ])
    password = PasswordField('password', validators=[
        InputRequired(message='Password is required'),
        Regexp('[A-Za-z0-9_!@#$%^&*?]{7,30}'),
        Length(min=7, max=30, message='Passwords must be at least 7 characters long')
    ])
    email = StringField('email', validators=[
        InputRequired(message='Email is required'),
        Email(message="Enter a valid email address")
    ])
    firstname = StringField('firstName', validators=[
        InputRequired(message='First Name is required'),
        Regexp('[A-Za-z]{2,20}', message='First name can only contain letter')
    ])
    lastname = StringField('lastName', validators=[
        InputRequired(message='Last Name is required'),
        Regexp('[A-Za-z]{2,20}', message='Last name can only contain letter')
    ])
    submit = SubmitField('Register')
