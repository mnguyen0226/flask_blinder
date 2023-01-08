from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# create a flask project
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret key"

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


# input user's name page and show it to another page
@app.route("/name", methods=["GET", "POST"])
def name():
    name = None
    form = NamerForm()

    # validate form, if submit then refresh data, also make sure that the user file out the form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""

    return render_template("name.html", name=name, form=form)


if __name__ == "__main__":
    app.run(debug=True)
