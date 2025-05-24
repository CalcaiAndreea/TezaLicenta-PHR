# recommendations.py
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, session, abort, flash
from db import db
from models import Recommendation, Patient, Doctor

recommend_bp = Blueprint("recommend_bp", __name__)

@recommend_bp.route("/doctor/patient/<int:pid>/add_reco", methods=["POST"])
def add_recommendation(pid):
    # autentificare medic
    if "user_id" not in session or session.get("role") != "doctor":
        return redirect(url_for("login_bp.login"))

    patient = Patient.query.get_or_404(pid)
    doctor  = Doctor.query.filter_by(user_id=session["user_id"]).first_or_404()

    text = request.form["reco_text"].strip()
    if not text:
        flash("Textul recomandării nu poate fi gol!", "danger")
        return redirect(url_for("doctor_bp.doctor_view_patient", pid=pid))

    reco = Recommendation(
        patient_id=patient.id,
        doctor_id=doctor.id,
        text=text,
        created_at=datetime.utcnow()
    )
    db.session.add(reco)
    db.session.commit()
    flash("Recomandare adăugată!", "success")
    return redirect(url_for("doctor_bp.doctor_view_patient", pid=pid))
