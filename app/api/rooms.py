from __future__ import annotations
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..extensions import db
from ..models.room import Room, RoomParticipant

bp = Blueprint("rooms", __name__)


@bp.get("")
@login_required
def list_rooms():
    rooms = Room.query.order_by(Room.created_at.desc()).limit(50).all()
    return jsonify([r.to_dict() for r in rooms])


@bp.post("/create")
@login_required
def create_room():
    data = request.get_json() or {}
    room = Room(
        title=data.get("title", "Untitled Room"),
        category=data.get("category", "general"),
        host_id=current_user.id,
        is_paid=bool(data.get("is_paid", False)),
        price_kes=int(data.get("price_kes", 0)),
    )
    db.session.add(room)
    db.session.commit()
    return jsonify(room.to_dict()), 201


@bp.post("/join")
@login_required
def join_room():
    data = request.get_json() or {}
    room_id = data.get("room_id")
    room = Room.query.get_or_404(room_id)

    if RoomParticipant.query.filter_by(room_id=room.id, user_id=current_user.id).first():
        return jsonify({"message": "already joined"})

    rp = RoomParticipant(room_id=room.id, user_id=current_user.id)
    db.session.add(rp)
    db.session.commit()
    return jsonify({"message": "joined"})


@bp.post("/tip")
@login_required
def tip_host():
    data = request.get_json() or {}
    room_id = data.get("room_id")
    amount = int(data.get("amount", 0))
    if amount <= 0:
        return {"error": "invalid amount"}, 400
    room = Room.query.get_or_404(room_id)
    # Handled by payments API in real integration
    return {"message": "tip accepted (mock)", "amount": amount, "host_id": room.host_id}
