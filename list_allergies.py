from flask import Blueprint, render_template, session, redirect, url_for, abort
from models import Patient, Allergy

list_allergies_bp = Blueprint("list_allergies_bp", __name__)

@list_allergies_bp.route("/patient/<int:pid>/allergies")
def list_allergies(pid):
    if "user_id" not in session or session.get("role") != "patient":
        return redirect(url_for("login_bp.login"))
    patient = Patient.query.filter_by(id=pid, user_id=session["user_id"]).first()
    if not patient:
        abort(403)
    allergies = Allergy.query.filter_by(patient_id=pid).order_by(
               Allergy.recorded_at.desc()).all()
    return render_template("list_allergies.html", patient=patient, allergies=allergies)
