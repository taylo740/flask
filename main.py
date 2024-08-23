from flask import Flask, session, redirect, url_for, render_template, request
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Login form to enter a room."""
    if "name" in request.form:
        session["name"] = request.form["name"]
        return redirect(url_for("chat"))
    elif request.method == "GET":
        name = session.get("name", "")
        return render_template("index.html", name=name)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
