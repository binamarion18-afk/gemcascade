from __future__ import annotations
from flask_socketio import emit, join_room as sio_join_room
from flask_login import current_user


def register_socket_events(socketio):
    @socketio.on("connect")
    def handle_connect():
        emit("connected", {"user_id": getattr(current_user, "id", None)})

    @socketio.on("room_joined")
    def on_room_joined(data):
        room = str(data.get("room_id"))
        sio_join_room(room)
        emit("room_joined", {"room": room, "user_id": getattr(current_user, "id", None)}, room=room)

    @socketio.on("message_sent")
    def on_message_sent(data):
        room = str(data.get("room_id"))
        text = data.get("text", "")
        emit("message_sent", {"room": room, "text": text, "user_id": getattr(current_user, "id", None)}, room=room)

    @socketio.on("payment_received")
    def on_payment_received(data):
        emit("payment_received", data, broadcast=True)

    @socketio.on("connection_made")
    def on_connection_made(data):
        emit("connection_made", data, broadcast=True)
