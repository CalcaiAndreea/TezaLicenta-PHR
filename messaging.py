# messaging.py
from datetime import datetime
from flask import Blueprint, render_template, session, redirect, url_for, request, abort
from db import db
from models import User, Patient, Doctor, Message

messaging_bp = Blueprint("messaging_bp", __name__)

# ------------------ inbox ------------------
@messaging_bp.route("/messages")
def inbox():
    if "user_id" not in session:
        return redirect(url_for("login_bp.login"))

    user_id = session["user_id"]
    role    = session["role"]

    # pentru medic – listăm toți pacienții; pentru pacient – un singur medic (primul găsit)
    if role == "doctor":
        partners = (
            db.session.query(User)
            .join(Patient, Patient.user_id == User.id)
            .order_by(User.email)
            .all()
        )
    else:  # patient
        # cautăm medicul asociat ultimelor programări sau orice doctor
        partners = (
            db.session.query(User)
              .join(Doctor, Doctor.user_id == User.id)
              .limit(1)
              .all()
        )

    return render_template("messages_overview.html", partners=partners)

# ------------------ thread patient<->doctor ------------------
@messaging_bp.route("/messages/<int:partner_id>")
def chat(partner_id):
    if "user_id" not in session:
        return redirect(url_for("login_bp.login"))

    me        = User.query.get_or_404(session["user_id"])
    partner   = User.query.get_or_404(partner_id)

    # extragem toate mesajele între cei doi, ordonate cronologic
    msgs = (
        Message.query
        .filter(
            ((Message.from_user_id == me.id) & (Message.to_user_id == partner.id)) |
            ((Message.from_user_id == partner.id) & (Message.to_user_id == me.id))
        )
        .order_by(Message.sent_at)
        .all()
    )
    return render_template("chat.html", me=me, partner=partner, messages=msgs)

# ------------------ POST send message ------------------
@messaging_bp.route("/messages/send", methods=["POST"])
def send_message():
    if "user_id" not in session:
        return redirect(url_for("login_bp.login"))

    content     = request.form["content"].strip()
    to_user_id  = int(request.form["to_user_id"])
    if not content:
        return redirect(url_for("messaging_bp.chat", partner_id=to_user_id))

    msg = Message(
        from_user_id=session["user_id"],
        to_user_id=to_user_id,
        content=content,
        sent_at=datetime.utcnow()
    )
    db.session.add(msg)
    db.session.commit()
    return redirect(url_for("messaging_bp.chat", partner_id=to_user_id))
