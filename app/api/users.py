from __future__ import annotations
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models.user import User, Interest, Skill, Connection

bp = Blueprint("users", __name__)


@bp.get("/profile")
@login_required
def get_profile():
    return jsonify(current_user.to_dict())


@bp.post("/profile")
@login_required
def update_profile():
    data = request.get_json() or {}
    current_user.bio = data.get("bio", current_user.bio)
    current_user.county = data.get("county", current_user.county)
    current_user.goals = data.get("goals", current_user.goals)
    db.session.commit()
    return jsonify(current_user.to_dict())


@bp.get("/match")
@login_required
def match_users():
    # Simple interest overlap matching for MVP
    interests = set(i.name for i in current_user.interests)
    if not interests:
        users = User.query.filter(User.id != current_user.id).limit(20).all()
        return jsonify([u.to_card_dict() for u in users])

    candidates = User.query.filter(User.id != current_user.id).all()
    scored = []
    for u in candidates:
        overlap = len(interests.intersection(set(i.name for i in u.interests)))
        if overlap:
            scored.append((overlap, u))
    scored.sort(key=lambda x: x[0], reverse=True)
    return jsonify([u.to_card_dict() for _, u in scored[:20]])


@bp.post("/connections")
@login_required
def add_connection():
    data = request.get_json() or {}
    target_id = data.get("user_id")
    if not target_id:
        return {"error": "user_id required"}, 400
    if target_id == current_user.id:
        return {"error": "cannot connect to self"}, 400

    existing = Connection.query.filter_by(user_id=current_user.id, target_user_id=target_id).first()
    if existing:
        return {"message": "already connected"}

    conn = Connection(user_id=current_user.id, target_user_id=target_id, strength=1)
    db.session.add(conn)
    db.session.commit()
    return {"message": "connected"}
