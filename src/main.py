from flask import Flask
from flask import render_template

# create a flask project
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/")
def user():
    name_list = ["Minh", "Tam", "Alex"]
    return render_template("user.html", user_name=name_list)

if __name__ == "__main__":
    app.run(debug=True)
