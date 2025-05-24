"""
login.py   – autentificare simplă, parole stocate direct în coloana password_hash
(NU sigur pentru producție – doar pentru demo local!)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User, Patient

login_bp = Blueprint("login_bp", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form["email"].strip().lower()
        password = request.form["password"]

        # căutăm utilizatorul
        user = User.query.filter_by(email=email).first()

        # ✔️ comparație directă cu textul din coloană
        if user and user.password_hash == password:
            session["user_id"] = user.id
            session["role"]    = user.role

            # redirecționăm după rol
            if user.role == "patient":
                patient = Patient.query.filter_by(user_id=user.id).first()
                session["patient_id"] = patient.id
                return redirect(url_for("patient_bp.dashboard_patient", pid=patient.id))
            elif user.role == "doctor":
                return redirect(url_for("doctor_bp.doctor_dashboard"))
            else:
                return redirect(url_for("home"))
        else:
            flash("Email sau parolă greșite", "danger")

    return render_template("login.html")


@login_bp.route("/logout")
def logout():
    session.clear()
    flash("Te-ai delogat.", "info")
    return redirect(url_for("login_bp.login"))
