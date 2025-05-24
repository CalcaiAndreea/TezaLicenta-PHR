from flask import Blueprint, render_template, session, redirect, url_for, abort
from models import Patient, VitalSign, Allergy, LabResult, Medication, Appointment

patient_bp = Blueprint("patient_bp", __name__)

@patient_bp.route("/patient/<int:pid>")
def dashboard_patient(pid):
    if "user_id" not in session or session.get("role") != "patient":
        return redirect(url_for("login_bp.login"))
    patient = Patient.query.filter_by(id=pid, user_id=session["user_id"]).first_or_404()
    context = dict(
        patient=patient,
        vitals=VitalSign.query.filter_by(patient_id=pid).order_by(
            VitalSign.recorded_at.desc()).all(),
        allergies=Allergy.query.filter_by(patient_id=pid).all(),
        lab_results=LabResult.query.filter_by(patient_id=pid).order_by(
            LabResult.collected_at.desc()).all(),
        medications=Medication.query.filter_by(patient_id=pid).all(),
        appointments=Appointment.query.filter_by(patient_id=pid).order_by(
            Appointment.appointment_date.desc()).all()
    )
    return render_template("patient_dashboard.html", **context)
