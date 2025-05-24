from flask import Blueprint, request, redirect, url_for, session, abort, flash
from models import Patient, Allergy
from db import db
from datetime import datetime

add_allergy_bp = Blueprint("add_allergy_bp", __name__)

@add_allergy_bp.route("/add_allergy", methods=["POST"])
def add_allergy():
    if "user_id" not in session or session.get("role") != "patient":
        return redirect(url_for("login_bp.login"))

    patient_id = request.form["patient_id"]
    patient = Patient.query.filter_by(id=patient_id, user_id=session["user_id"]).first()
    if not patient:
        abort(403)

    allergy = Allergy(
        patient_id=patient_id,
        substance=request.form["substance"],
        reaction=request.form.get("reaction", ""),
        severity=request.form.get("severity", "mild"),
        recorded_at=datetime.utcnow()
    )
    db.session.add(allergy)
    db.session.commit()
    flash("Alergie adăugată!", "success")
    return redirect(url_for("patient_bp.dashboard_patient", pid=patient_id))
