import eventlet
eventlet.monkey_patch()

from flask import Flask, session, redirect, url_for, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

from Game import Game



socketio = SocketIO()

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "gjr39dkjn344_!67#"
app.port = os.getenv("PORT", default=5000)

game = Game()

@socketio.on("joined", namespace="/chat")
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    join_room(session.get("name"))
    game.user_login(session.get("name"))


@socketio.on("text", namespace="/chat")
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    game.on_message(session.get("name"), message["msg"])


@socketio.on("left", namespace="/chat")
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    leave_room(session.get("name"))
    game.user_leave(session.get("name"))


@app.route("/", methods=["GET", "POST"])
def index():
    """Login form to enter a room."""
    if "name" in request.form:
        session["name"] = request.form["name"]
        return redirect(url_for("chat"))
    elif request.method == "GET":
        name = session.get("name", "")
        return render_template("index.html", name=name)


@app.route("/chat")
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get("name", "")
    if name == "":
        return redirect(url_for("index"))
    return render_template("chat.html", name=name)

socketio.init_app(app, cors_allowed_origins="*", async_mode='eventlet')

if __name__ == '__main__':
    socketio.run(app)
