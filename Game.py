from flask_socketio import SocketIO, emit, join_room, leave_room


class Game:
    def __init__(self):
        self.active_users = {}

    def user_login(self, user):
        self.active_users[user] = True

    def user_leave(self, user):
        del self.active_users[user]

    def get_active_users(self):
        return list(self.active_users.keys())

    def send_to_users(self, users, text):
        for user in users:
            emit("message", {"msg": text}, to=user)
            print("user", user, text)

    def on_message(self, user, text: str):
        if text.startswith("/w"):
            w, who, what = text.split(" ", 2)
            self.send_to_users([who, user], user + ' whispers: "' + what + '"')
        else:
            self.send_to_users(self.get_active_users(), user + ": " + text)
