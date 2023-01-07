from flask import Flask
from flask import render_template

# create a flask project
app = Flask(__name__)

# home page
@app.route("/")
def index():
    return render_template("index.html")

# user page
@app.route("/user/")
def user():
    name_list = ["Minh", "Tam", "Alex"]
    return render_template("user.html", user_name=name_list)

# invalid url page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# internal server error page
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)
