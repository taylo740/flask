from flask import Flask, session, redirect, url_for, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

socketio = SocketIO()

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "gjr39dkjn344_!67#"
app.port = os.getenv("PORT", default=5000)


@app.route("/", methods=["GET", "POST"])
def index():
    """Login form to enter a room."""
    if "name" in request.form:
        session["name"] = request.form["name"]
        return redirect(url_for("chat"))
    elif request.method == "GET":
        name = session.get("name", "")
        return render_template("index.html", name=name)

socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app)
