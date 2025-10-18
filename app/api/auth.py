from __future__ import annotations
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from ..extensions import db
from ..models.user import User

bp = Blueprint("auth", __name__)


@bp.post("/register")
def register():
    data = request.get_json() or {}
    required = ["email", "password", "name"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(email=data["email"], name=data["name"], phone=data.get("phone"))    
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict(include_private=False)), 201


@bp.post("/login")
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"error": "Invalid credentials"}), 401
    login_user(user)
    return jsonify(user.to_dict(include_private=False))


@bp.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})
