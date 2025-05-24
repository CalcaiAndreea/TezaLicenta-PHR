from flask import Blueprint, render_template, session, redirect, url_for, abort
from models import (Patient, VitalSign, Allergy,
                    LabResult, Medication, Appointment)

doctor_bp = Blueprint("doctor_bp", __name__)

@doctor_bp.route("/doctor")
def doctor_dashboard():
    if "user_id" not in session or session.get("role") != "doctor":
        return redirect(url_for("login_bp.login"))
    patients = Patient.query.order_by(Patient.last_name).all()
    return render_template("doctor_dashboard.html", patients=patients)

@doctor_bp.route("/doctor/patient/<int:pid>")
def doctor_view_patient(pid):
    if "user_id" not in session or session.get("role") != "doctor":
        return redirect(url_for("login_bp.login"))
    patient = Patient.query.get_or_404(pid)
    data = dict(
        patient=patient,
        vitals=VitalSign.query.filter_by(patient_id=pid)
                              .order_by(VitalSign.recorded_at.desc()).all(),
        allergies=Allergy.query.filter_by(patient_id=pid).all(),
        lab_results=LabResult.query.filter_by(patient_id=pid)
                                   .order_by(LabResult.collected_at.desc()).all(),
        medications=Medication.query.filter_by(patient_id=pid).all(),
        appointments=Appointment.query.filter_by(patient_id=pid)
                                       .order_by(Appointment.appointment_date.desc()).all()
    )
    return render_template("doctor_view_patient.html", **data)
