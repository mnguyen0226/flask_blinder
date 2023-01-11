from flask import Flask
from flask import render_template
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import ValidationError
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, date
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea
from flask import redirect, url_for
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)

# create a flask project
app = Flask(__name__)

# init database as sqlite
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# init database as mysql
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://username:password@localhost/db_name"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:password123@localhost/our_users"

# init secret key
app.config["SECRET_KEY"] = "secret key"

# create database
db = SQLAlchemy(app)

# migrate our app with current database (aka, update database)
migrate = Migrate(app, db)
app.app_context().push()

# Page to return JSON - we can actually build an API with JSON
@app.route("/date")
def get_current_date():
    favorite_pizza = {
        "John": "Pepperoni",
        "Mary": "Cheese",
        "Tim": "Mushroom",
    }
    return {favorite_pizza}


# create database model - add UserMixin for login and session
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(
        db.String(200), nullable=False, unique=True
    )  # if not, will not be added to the database
    fav_color = db.Column(db.String(120), nullable=True)
    date_added = db.Column(
        db.DateTime, default=datetime.utcnow
    )  # date that they created, not update tho

    # set up password
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        # this so that when the user try to view the password with "user.password", will get the error message
        raise AttributeError("password is not a readable attribute!")

    @password.setter
    def password(self, password):
        # hash the user's input password
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # verify input password
        return check_password_hash(self.password_hash, password)

    # create a string representation of object for debugging
    def __repr__(self):
        return "<Name %r>" % self.name


# create a blog post model - similar to form
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())
    slug = db.Column(
        db.String(255)
    )  # instead of url "/post/3" it can be "/post/third_post"


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


# Flask_Login Backend: session
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # function login()


@login_manager.user_loader
def load_user(user_id):
    # to load user, we need to query database
    return Users.query.get(int(user_id))


# create a login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("What's Your Password?", validators=[DataRequired()])
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


# allow to enter a user info and show in the same page. Mini Project 1: Patient Register
@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()

    # POST request
    if request.method == "POST":
        # if form is submit and valid (unique as ourssting)
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()

            # if there is not a user (based on unique values then you can create a new user)
            if user is None:

                # hash password
                hashed_pw = generate_password_hash(
                    form.password_hash.data, "sha256"
                )  # sha256 is the name of algorithm for hashing in cryptography

                # create a new user (row in database)
                new_user = Users(
                    name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    fav_color=form.fav_color.data,
                    password_hash=hashed_pw,
                )

                # add to database
                db.session.add(new_user)
                db.session.commit()

                # get name from form
                name = form.name.data
                flash("User Added Successfully!")

            else:
                flash(
                    "Error: This email has been taken, not added to database. Please choose another email"
                )

            # reset info
            form.name.data = ""
            form.username.data = ""
            form.email.data = ""
            form.fav_color.data = ""
            form.password_hash.data = ""

        # get users ordered by date
        our_users = Users.query.order_by(Users.date_added)

        return render_template(
            "add_user.html", form=form, name=name, our_users=our_users
        )

    # GET request
    else:
        our_users = Users.query.order_by(Users.date_added)

        return render_template(
            "add_user.html", form=form, name=name, our_users=our_users
        )


# update database record for user info
@app.route("/update/<int:id>", methods=["GET", "POST"])  # mini project 1: Patient Info
def update(id):
    form = UserForm()

    # try to find the user info from database
    name_to_update = Users.query.get_or_404(id)

    # POST: if the user fill out the form and send the information back to database
    if request.method == "POST":
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.fav_color = request.form["fav_color"]

        # if the infromation is update successfully, we return back to the users register page
        try:
            db.session.commit()
            flash(" Updated Successfully!")
            return render_template(
                "update.html", form=form, name_to_update=name_to_update
            )
        # if we can't then stay at the same page and try again
        except:
            flash("Error: Can't update. Try again!")
            return render_template(
                "update.html", form=form, name_to_update=name_to_update
            )
    # GET: if they just go (or refresh), then just render the curretn page
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update)


# delete the record from the database
# note that for delete, there is no need for post or get as once we click (aka, access the page), we will delete the record, no
@app.route("/delete/<int:id>")
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        # delete from db
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")

        # get users ordered by date
        our_users = Users.query.order_by(Users.date_added)

        return render_template(
            "add_user.html", form=form, name=name, our_users=our_users
        )

    except:
        flash("Error: Unable to delete user. Try again.")
        return render_template(
            "add_user.html", form=form, name=name, our_users=our_users
        )


# testing page to test and validate matching input. if match then render user's page.
@app.route("/test_pw", methods=["GET", "POST"])
def test_pw():
    # initialize input variable and form object
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    # if the user (must) fill out the form, then we get the name variable and reset the form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data

        form.email.data = ""
        form.password_hash.data = ""
        # flash("Form Submitted Successfully!")

        # get the password based on user
        pw_to_check = Users.query.filter_by(email=email).first()

        # check hashed password:
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template(
        "test_pw.html",
        email=email,
        password=password,
        form=form,
        pw_to_check=pw_to_check,
        passed=passed,
    )


# Add Post Page
@app.route("/add-post", methods=["GET", "POST"])
def add_post():
    form = PostForm()

    # if the user fill out the form, we will fillout in the database
    if form.validate_on_submit():
        post = Posts(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data,
            slug=form.slug.data,
        )

        # clear form
        form.title.data = ""
        form.content.data = ""
        form.author.data = ""
        form.slug.data = ""

        # add a new row to database
        db.session.add(post)
        db.session.commit()

        flash("Blog Post Submitted Successfully!")

    return render_template("add_post.html", form=form)


# create a page to view all posts
@app.route("/posts")
def posts():
    # get all posts from database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)


# create a page that allow to
@app.route("/posts/<int:id>")
def post(id):
    # found the post from the id
    post = Posts.query.get_or_404(id)
    return render_template("post.html", post=post)


# update database record for single blog post
@app.route("/posts/edit/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    form = PostForm()

    # if the user fill out the form and send the info back to database
    post_to_update = Posts.query.get_or_404(id)

    # POST
    if form.validate_on_submit():
        # update in the database
        post_to_update.title = form.title.data
        post_to_update.author = form.author.data
        post_to_update.slug = form.slug.data
        post_to_update.content = form.content.data

        # commit to the database
        db.session.add(post_to_update)
        db.session.commit()

        flash("Post Updated Successfully!")

        # can render instead of redirect. go back to the single blog post
        return redirect(url_for("post", id=post_to_update.id))

    # you can do this or just pass in "post_to_update" with the fill out value (similar to update.html)
    form.title.data = post_to_update.title
    form.author.data = post_to_update.author
    form.slug.data = post_to_update.slug
    form.content.data = post_to_update.content

    return render_template("edit_post.html", form=form)


# feature allow to delete post
@app.route("/posts/delete/<int:id>")
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    posts = Posts.query.order_by(Posts.date_posted)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()

        flash("Blog Deleted Successfully!")

        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
    except:
        flash("Error: Unable to delete blog post. Try again.")
        return render_template("posts.html", posts=posts)


# PAGE: login page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    # if the user fill out the form
    if form.validate_on_submit():

        # get the first user name
        user = Users.query.filter_by(username=form.username.data).first()

        # if found user in the database
        if user:
            # if the password match
            filled_password = form.password.data

            if check_password_hash(user.password_hash, filled_password):
                # the pacage will login and create a session
                flash("Correct Password! Log in Successfully!")
                login_user(user)
                return redirect(url_for("dashboard"))
            else:
                flash("Wrong Password! Fail to Log in!")

        # if does not find the user in the database
        else:
            flash("Username Does Not Exist! Try Again!")

    return render_template("login.html", form=form)


# PAGE: dashboard page
@app.route("/dashboard", methods=["GET", "POST"])
@login_required  # just make sure that we have to login first before go to dashboard
def dashboard():
    return render_template("dashboard.html")


# logout
@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()  # sqlite or mysql
    app.run(debug=True)
