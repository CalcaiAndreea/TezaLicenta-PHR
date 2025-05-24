from flask import Blueprint, render_template, session, redirect, url_for, abort
from models import Patient, VitalSign

list_vitals_bp = Blueprint("list_vitals_bp", __name__)

@list_vitals_bp.route("/patient/<int:pid>/vitals")
def list_vitals(pid):
    if "user_id" not in session or session.get("role") != "patient":
        return redirect(url_for("login_bp.login"))
    patient = Patient.query.filter_by(id=pid, user_id=session["user_id"]).first()
    if not patient:
        abort(403)
    vitals = VitalSign.query.filter_by(patient_id=pid).order_by(
             VitalSign.recorded_at.desc()).all()
    return render_template("list_vitals.html", patient=patient, vitals=vitals)
