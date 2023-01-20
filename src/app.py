from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
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
import uuid as uuid
import os

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

# set image update (must put here)
UPLOAD_FOLDER = "static/user_images/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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

        return render_template("sign_up.html", form=form)

    # get request
    else:
        return render_template("sign_up.html", form=form)


@app.route("/delete/<int:id>")
def delete(id):
    form = UserForm()

    # get user from id
    user_to_delete = Users.query.get_or_404(id)

    # from the user, get all the ids of the post
    posts_to_delete = Posts.query.filter(Posts.poster_id.like(id)).all()

    try:
        for post in posts_to_delete:
            db.session.delete(post)
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully!")
        return render_template("sign_up.html", form=form)

    except:
        flash(
            "Error: Unable to delete user as the user does not exist or error in access posts!"
        )
        return render_template("sign_up.html", form=form)


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
        name_to_update.about_author = request.form["about_author"]

        # if there is a request for new image, update the database with image
        if request.files["profile_pic"]:

            # get the name of the image
            name_to_update.profile_pic = request.files["profile_pic"]

            # the two steps below basically convert image file to just get name
            # get image name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)

            # set uuid - get random number to get unique name
            pic_name = str(uuid.uuid1()) + "_" + pic_filename

            # save image
            saver = request.files["profile_pic"]

            # change string to save in the database
            name_to_update.profile_pic = pic_name

            # if the infromation is update successfully, we return back to the users register page
            try:
                db.session.commit()

                # save the image in the local file
                saver.save(os.path.join(app.config["UPLOAD_FOLDER"], pic_name))

                flash(" Updated Successfully!")
                return render_template(
                    "dashboard.html", form=form, name_to_update=name_to_update
                )

            # if we can't then stay at the same page and try again
            except:
                flash("Error: Can't update. Try again!")
                return render_template(
                    "dashboard.html", form=form, name_to_update=name_to_update
                )

        # if we don't update the image, then just commit other info
        else:
            db.session.commit()
            flash(" Updated Successfully!")
            return render_template(
                "dashboard.html", form=form, name_to_update=name_to_update
            )

    # GET: if they just go (or refresh), then just render the curretn page
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
        return render_template("view_post.html", posts=posts)


# delete post
@app.route("/posts/delete/<int:id>")
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    # if the current login user id == the id of the blog's author's id
    if current_user.id == post_to_delete.poster.id or current_user.id == 3:

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
    users_list = Users.query.order_by(Users.date_added)

    if id == 3:
        return render_template("admin.html", users_list=users_list)
    else:
        flash("Error: Must be admin to access this page!")
        return redirect(url_for("dashboard"), users_list=users_list)


# view specific post
@app.route("/dashboard/<int:id>")
def view_dashboard(id):
    user = Users.query.get_or_404(id)
    return render_template("view_user.html", user=user)


@app.route("/like-post/<post_id>", methods=["POST"])
@login_required
def like(post_id):
    post = Posts.query.filter_by(id=post_id).first()

    # get the lke from the current user and all likes from other post that he/she likes
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({"error": "post does not exist!"}, 400)  # 400 = bad request
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    # send the json to js file
    # return redirect(url_for("view_all_posts.html"))
    return jsonify(
        {
            "likes": len(post.likes),
            "liked": current_user.id in map(lambda x: x.author, post.likes),
        }
    )


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

    # author description
    about_author = db.Column(db.Text(500), nullable=True)

    # profile pic dir - can't define the size tho.
    profile_pic = db.Column(db.String(1000), nullable=True)

    # many-to-many relationship
    likes = db.relationship("Like", backref="user", passive_deletes=True)

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

    # many-to-many relationship
    likes = db.relationship("Like", backref="post", passive_deletes=True)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # similar to poster_id in Posts
    author = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    post_id = db.Column(
        db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
