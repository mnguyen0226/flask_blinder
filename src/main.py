from flask import Flask
from flask import render_template
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create a flask project
app = Flask(__name__)

# init database as sqlite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# init secret key
app.config["SECRET_KEY"] = "secret key"

# create database
db = SQLAlchemy(app)
app.app_context().push()

# create database model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(
        db.DateTime, default=datetime.utcnow
    )  # date that they created, not update tho

    # create a string representation of object for debugging
    def __repr__(self):
        return "<Name %r>" % self.name


class UserForm(FlaskForm):
    name = StringField("Enter Name", validators=[DataRequired()])
    email = StringField("Enter Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


# create a form class for input submission
class NamerForm(FlaskForm):
    name = StringField("What's Your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# home page
@app.route("/")
def index():
    return render_template("index.html")


# user page
@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)


# invalid url page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# internal server error page
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# input user's name page and show it to the current
@app.route("/name", methods=["GET", "POST"])
def name():
    # initialize input variable and form object
    name = None
    form = NamerForm()

    # if the user (must) fill out the form, then we get the name variable and reset the form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form Submitted Successfully!")

    return render_template("name.html", name=name, form=form)


# allow to enter a user info and show in the same page
@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()

    # if form is submit and valid (unique as ourssting)
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        # if there is not a user (based on unique values then you can create a new user)
        if user is None:
            new_user = Users(name=form.name.data, email=form.email.data)
            db.session.add(new_user)
            db.session.commit()

        # get name from form
        name = form.name.data

        # reset info
        form.name.data = ""
        form.email.data = ""

    # get users ordered by date
    our_users = Users.query.order_by(Users.date_added)

    return render_template("add_user.html", form=form, name=name, our_users=our_users)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
