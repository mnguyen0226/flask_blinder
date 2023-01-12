# file contains all forms
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms import SubmitField
from wtforms import StringField
from wtforms import PasswordField
from wtforms.widgets import TextArea


class UserForm(FlaskForm):
    name = StringField("Enter Name", validators=[DataRequired()])
    username = StringField("Enter UserName", validators=[DataRequired()])
    email = StringField("Enter Email", validators=[DataRequired()])
    fav_color = StringField("Enter Color", validators=[DataRequired()])

    # need 2 password 1 for enter, 1 for confirm the same typed password
    password_hash = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password_hash2", message="Passwords Must Match!"),
        ],
    )
    password_hash2 = PasswordField(
        "Confirm Password", validators=[DataRequired()]
    )  # does not exist in the actual database

    submit = SubmitField("Submit")


# create a form class for input submission
class NamerForm(FlaskForm):
    name = StringField("What's Your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# create a form class to test for password
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email?", validators=[DataRequired()])
    password_hash = PasswordField("What's Your Password?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# create a post form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


# create a login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("What's Your Password?", validators=[DataRequired()])
    submit = SubmitField("Submit")
