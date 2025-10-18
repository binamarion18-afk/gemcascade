from __future__ import annotations
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models.gig import Gig, GigApplication

bp = Blueprint("gigs", __name__)


@bp.get("")
@login_required
def list_gigs():
    gigs = Gig.query.order_by(Gig.created_at.desc()).limit(50).all()
    return jsonify([g.to_dict() for g in gigs])


@bp.post("/create")
@login_required
def create_gig():
    data = request.get_json() or {}
    gig = Gig(
        title=data.get("title", "Untitled Gig"),
        description=data.get("description", ""),
        budget_kes=int(data.get("budget_kes", 0)),
        poster_id=current_user.id,
    )
    db.session.add(gig)
    db.session.commit()
    return jsonify(gig.to_dict()), 201


@bp.post("/apply")
@login_required
def apply_gig():
    data = request.get_json() or {}
    gig_id = data.get("gig_id")
    gig = Gig.query.get_or_404(gig_id)
    if GigApplication.query.filter_by(gig_id=gig.id, applicant_id=current_user.id).first():
        return {"message": "already applied"}
    appn = GigApplication(gig_id=gig.id, applicant_id=current_user.id, pitch=data.get("pitch", ""))
    db.session.add(appn)
    db.session.commit()
    return {"message": "applied"}
