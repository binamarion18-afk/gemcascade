from __future__ import annotations
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..services.mpesa import stk_push

bp = Blueprint("payments", __name__)


@bp.post("/mpesa/request")
@login_required
def mpesa_request():
    data = request.get_json() or {}
    msisdn = data.get("msisdn") or getattr(current_user, "phone", None)
    amount = int(data.get("amount", 0))
    if not msisdn or amount <= 0:
        return jsonify({"error": "msisdn and positive amount required"}), 400
    try:
        resp = stk_push(msisdn=msisdn, amount=amount, account_ref=str(current_user.id), tx_desc="Chooza payment")
        return jsonify({"status": "initiated", "mpesa": resp}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 502


@bp.post("/callback")
def mpesa_callback():
    payload = request.get_json() or {}
    # Log and acknowledge
    return jsonify({"status": "received", "payload": payload}), 200
