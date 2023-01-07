from flask import Flask
from flask import render_template

# create a flask project
app = Flask(__name__)


@app.route("/")
def index():
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True)
