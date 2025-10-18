from __future__ import annotations
from datetime import datetime
from ..extensions import db


class Gig(db.Model):
    __tablename__ = "gigs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    budget_kes = db.Column(db.Integer, default=0)
    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "budget_kes": self.budget_kes,
            "poster_id": self.poster_id,
            "created_at": self.created_at.isoformat() + "Z",
        }


class GigApplication(db.Model):
    __tablename__ = "gig_applications"
    id = db.Column(db.Integer, primary_key=True)
    gig_id = db.Column(db.Integer, db.ForeignKey("gigs.id"), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    pitch = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
