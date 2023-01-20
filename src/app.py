from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_ckeditor import CKEditor
from webforms import UserForm, LoginForm, PostForm, SearchForm


#############################################
# SET UP
#############################################
# set up Flask
app = Flask(__name__)

# config mysql
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:password123@localhost/flask_hacker_news"
app.config["SECRET_KEY"] = "secret key"

# create databse
db = SQLAlchemy(app)

# set up database migration
migrate = Migrate(app, db)
app.app_context().push()

# set up user login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# set up rich text
ckeditor = CKEditor(app)

# login manager
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# link form from base.html to navbar search bar
@app.context_processor
def base_link_form():
    form = SearchForm()
    return dict(form=form)


#############################################
# ROUTES
#############################################
# home page
@app.route("/")
def index():
    return render_template("index.html")


# 404 error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# sign up
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = UserForm()

    # TODO: move this list to admin page
    users_list = Users.query.order_by(Users.date_added)

    # post request
    if request.method == "POST":

        # if the user fill out the form correctly
        if form.validate_on_submit():

            # search the user by email
            user = Users.query.filter_by(email=form.email.data).first()

            # if a new user, add to the database
            if user is None:

                hashed_pw = generate_password_hash(form.password_create.data, "sha256")

                new_user = Users(
                    name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    hashed_password=hashed_pw,
                )

                db.session.add(new_user)
                db.session.commit()
                flash("New user signed up successfully!")

            else:
                flash("Error: This email has been taken. Please choose another email!")

            # reset the form
            form.name.data = ""
            form.username.data = ""
            form.email.data = ""
            form.password_create.data = ""
            form.password_confirm.data = ""

        # update the new database
        users_list = Users.query.order_by(Users.date_added)
        return render_template("sign_up.html", form=form, users_list=users_list)

    # get request
    else:
        return render_template("sign_up.html", form=form, users_list=users_list)


@app.route("/delete/<int:id>")
def delete(id):
    # get user from id
    user_to_delete = Users.query.get_or_404(id)
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully!")

        # update user list
        users_list = Users.query.order_by(Users.date_added)
        return render_template("sign_up.html", form=form, users_list=users_list)

    except:
        flash("Error: Unable to delete user as the user does not exist!")

        users_list = Users.query.order_by(Users.date_added)
        return render_template("sign_up.html", form=form, users_list=users_list)


# login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    # if the user fill out the form correctly
    if form.validate_on_submit():

        # query the user base on username
        found_username = Users.query.filter_by(username=form.username.data).first()

        if found_username:
            filled_password = form.password.data
            if check_password_hash(found_username.hashed_password, filled_password):
                flash("Login successfully!")
                login_user(found_username)
                return redirect(url_for("dashboard"))

            else:
                flash("Error: Wrong password. Try again!")
        else:
            flash("Error: Username does not exist. Try again!")
    return render_template("login.html", form=form)


# user dashboard
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)

    # post
    if request.method == "POST":
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.username = request.form["username"]

        try:
            db.session.commit()
            flash("Profile updated successfully!")
            return render_template(
                "dashboard.html", form=form, name_to_update=name_to_update
            )
        except:
            flash("Error: Can't update. Try again!")
            return render_template(
                "dashboard.html", form=form, name_to_update=name_to_update
            )
    else:
        return render_template(
            "dashboard.html", form=form, name_to_update=name_to_update
        )


# logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for("login"))


# create a post
@app.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()

    # if the user properly fill out the post
    if form.validate_on_submit():

        # get logged in user id
        poster = current_user.id

        # fill out the form
        post = Posts(
            title=form.title.data, content=form.content.data, poster_id=poster,
        )

        # clear form
        form.title.data = ""
        form.content.data = ""

        # commit to sql database
        db.session.add(post)
        db.session.commit()

        flash("Post submitted successfully!")

    return render_template("create_post.html", form=form)


# view all created post
@app.route("/posts")
def view_all_posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("view_all_posts.html", posts=posts)


# view specific post
@app.route("/posts/<int:id>")
def view_post(id):
    post = Posts.query.get_or_404(id)
    return render_template("view_post.html", post=post)


# update content in blog post
@app.route("/posts/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    form = PostForm()

    post_to_update = Posts.query.get_or_404(id)

    # if login the right person
    if current_user.id == post_to_update.poster_id:

        if form.validate_on_submit():
            # update the database
            post_to_update.title = form.title.data
            post_to_update.content = form.content.data

            # commit to database
            db.session.add(post_to_update)
            db.session.commit()

            flash("Post updated successfully!")

            return redirect(url_for("view_post", id=post_to_update.id))

        # here, the user has login, we just prefill, but not enable to fill form (if not a right person)
        form.title.data = post_to_update.title
        form.content.data = post_to_update.content
        return render_template("edit_post.html", form=form)

    else:
        flash("Error: You aren't authorized to edit page!")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)


# delete post
@app.route("/posts/delete/<int:id>")
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    # if the current login user id == the id of the blog's author's id
    if current_user.id == post_to_delete.poster.id:

        try:
            db.session.delete(post_to_delete)
            db.session.commit()

            flash("Blog deleted successfully!")

            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("view_all_posts.html", posts=posts)

        except:
            flash("Error: Unable to delete blog post. Try again.")
            return render_template("view_all_posts.html", posts=posts)
    else:
        flash("You aren't authorize to delete that post!")

        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("view_all_posts.html", posts=posts)


# basically a replicate of "view all post" after search
@app.route("/search", methods=["POST"])
def search():
    form = SearchForm()

    posts = Posts.query

    # if someone fillout the form
    if form.validate_on_submit():

        filled_search = form.searched.data

        # query the database
        posts = posts.filter(Posts.content.like("%" + filled_search + "%"))
        posts = posts.order_by(Posts.title).all()

        return render_template(
            "search.html", form=form, filled_search=filled_search, posts=posts
        )

# set up admin page
@app.route("/admin")
@login_required
def admin():
    id = current_user.id  # admin has id == 1

    if id == 3:
        return render_template("admin.html")
    else:
        flash("Error: Must be admin to access this page!")
        return redirect(url_for("dashboard"))

#############################################
# DATABASES
#############################################
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    hashed_password = db.Column(db.String(128))

    # one-to-many relationship
    posts = db.relationship("Posts", backref="poster")

    # overwrite getter
    @property
    def password(self):
        raise AttributeError("Error: password is not a readable attribute.")

    # hash password
    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    # verify password
    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    # overwrite print()
    def __repr__(self):
        return f"<Name: {self.name}> (Debug)"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())

    # connect secondary key to primary key
    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
