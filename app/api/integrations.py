from __future__ import annotations
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

bp = Blueprint("integrations", __name__)


@bp.post("/whatsapp/sync")
@login_required
def whatsapp_sync():
    data = request.get_json() or {}
    contacts = data.get("contacts", [])
    # Simulate sync: acknowledge number of contacts
    return jsonify({"synced": len(contacts), "user_id": current_user.id})


@bp.post("/ussd/session")
def ussd_session():
    # Minimal USSD stub for fallback flows
    payload = request.get_json() or {}
    text = payload.get("text", "")
    if text == "":
        response = "CON Karibu Chooza! 1. Register 2. Gigs 3. Exit"
    elif text == "1":
        response = "END Tafadhali tembelea app chooza.ke kujiandikisha"
    elif text == "2":
        response = "END Tembelea app kuona kazi mpya"
    else:
        response = "END Asante kwa kutumia Chooza"
    return jsonify({"response": response})
