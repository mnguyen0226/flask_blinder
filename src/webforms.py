from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo
from wtforms import SubmitField, StringField, PasswordField
from flask_ckeditor import CKEditorField

# sign up form
class UserForm(FlaskForm):
    name = StringField("Enter Name", validators=[DataRequired()])
    username = StringField("Enter Username", validators=[DataRequired()])
    email = StringField("Enter Email", validators=[DataRequired()])
    password_create = PasswordField(
        "Enter New Password",
        validators=[
            DataRequired(),
            EqualTo("password_confirm", message="Password Must Match!"),
        ],
    )
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# login form
class LoginForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# post form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")


# search form
class SearchForm(FlaskForm):
    searched = StringField("What are you looking for?", validators=[DataRequired()])
    submit = SubmitField()
