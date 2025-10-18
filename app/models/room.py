from __future__ import annotations
from datetime import datetime
from ..extensions import db


class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(80), default="general")
    host_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    is_paid = db.Column(db.Boolean, default=False)
    price_kes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "host_id": self.host_id,
            "is_paid": self.is_paid,
            "price_kes": self.price_kes,
            "created_at": self.created_at.isoformat() + "Z",
        }


class RoomParticipant(db.Model):
    __tablename__ = "room_participants"
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
