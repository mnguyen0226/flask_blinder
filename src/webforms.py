from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo
from wtforms import SubmitField, StringField, PasswordField, TextAreaField
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
from wtforms.widgets import TextArea

# sign up form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_create = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            EqualTo("password_confirm", message="Password Must Match!"),
        ],
    )
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired()])

    about_author = TextAreaField("About Author")

    profile_pic = FileField("Upload Profile Picture")

    submit = SubmitField("Submit")


# login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# post form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    # content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")


# search form
class SearchForm(FlaskForm):
    searched = StringField("What are you looking for?", validators=[DataRequired()])
    submit = SubmitField()
