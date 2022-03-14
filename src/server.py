from flask import Flask, render_template, jsonify, request, Response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add-todo/", methods=["POST"])
def add_todo():
    x = 1


@app.route("/todos/", methods=["GET"])
def get_todos():
    x = 1


if __name__ == '__main__':
    app.run()
