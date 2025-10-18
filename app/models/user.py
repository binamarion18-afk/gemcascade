from __future__ import annotations
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from ..extensions import db, login_manager


user_interest = db.Table(
    "user_interest",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("interest_id", db.Integer, db.ForeignKey("interests.id"), primary_key=True),
)

user_skill = db.Table(
    "user_skill",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("skill_id", db.Integer, db.ForeignKey("skills.id"), primary_key=True),
)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, default="")
    county = db.Column(db.String(80), default="")
    goals = db.Column(db.Text, default="")
    clout_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    interests = db.relationship("Interest", secondary=user_interest, backref="users", lazy="joined")
    skills = db.relationship("Skill", secondary=user_skill, backref="users", lazy="joined")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_private: bool = False) -> dict:
        data = {
            "id": self.id,
            "email": self.email if include_private else None,
            "phone": self.phone if include_private else None,
            "name": self.name,
            "bio": self.bio,
            "county": self.county,
            "goals": self.goals,
            "clout_score": self.clout_score,
            "interests": [i.name for i in self.interests],
            "skills": [s.name for s in self.skills],
            "created_at": self.created_at.isoformat() + "Z",
        }
        if not include_private:
            data.pop("email", None)
            data.pop("phone", None)
        return data

    def to_card_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "county": self.county,
            "clout_score": self.clout_score,
            "interests": [i.name for i in self.interests][:5],
            "skills": [s.name for s in self.skills][:5],
        }


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))


class Interest(db.Model):
    __tablename__ = "interests"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class Skill(db.Model):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class Connection(db.Model):
    __tablename__ = "connections"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    target_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    strength = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
