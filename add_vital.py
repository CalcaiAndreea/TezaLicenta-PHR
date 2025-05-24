from datetime import datetime
from flask import Blueprint, request, redirect, url_for, session, abort, flash
from models import Patient, VitalSign
from db import db

add_vital_bp = Blueprint("add_vital_bp", __name__)

@add_vital_bp.route("/add_vital", methods=["POST"])
def add_vital():
    if "user_id" not in session or session.get("role") != "patient":
        return redirect(url_for("login_bp.login"))

    patient_id = request.form["patient_id"]
    patient = Patient.query.filter_by(id=patient_id, user_id=session["user_id"]).first()
    if not patient:
        abort(403)

    vs = VitalSign(
        patient_id=patient_id,
        sign_type=request.form["sign_type"],
        sign_value=request.form["sign_value"],
        unit=request.form.get("unit", ""),
        recorded_at=datetime.utcnow()
    )
    db.session.add(vs)
    db.session.commit()
    flash("Semn vital adăugat!", "success")
    return redirect(url_for("patient_bp.dashboard_patient", pid=patient_id))
