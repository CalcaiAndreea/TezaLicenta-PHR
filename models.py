from datetime import datetime
from db import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("patient", "doctor", "admin"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.Enum("male", "female", "other"))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    user = db.relationship("User", backref=db.backref("patient_profile", uselist=False))

class Doctor(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    office_address = db.Column(db.Text)
    user = db.relationship("User", backref=db.backref("doctor_profile", uselist=False))

class Allergy(db.Model):
    __tablename__ = "allergies"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    substance = db.Column(db.String(255), nullable=False)
    reaction = db.Column(db.Text)
    severity = db.Column(db.Enum("mild", "moderate", "severe"))
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient = db.relationship("Patient", backref="allergies")

class MedicalHistory(db.Model):
    __tablename__ = "medical_history"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    condition_name = db.Column(db.String(255), nullable=False)
    diagnosis_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    patient = db.relationship("Patient", backref="medical_history")

class Medication(db.Model):
    __tablename__ = "medications"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    medication_name = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    prescribing_doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    patient = db.relationship("Patient", backref="medications")
    prescriber = db.relationship("Doctor")

class VitalSign(db.Model):
    __tablename__ = "vital_signs"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    sign_type = db.Column(db.String(50), nullable=False)
    sign_value = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20))
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient = db.relationship("Patient", backref="vital_signs")

class LabResult(db.Model):
    __tablename__ = "lab_results"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    result_type = db.Column(db.String(100), nullable=False)
    result_value = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(50))
    collected_at = db.Column(db.DateTime)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    patient = db.relationship("Patient", backref="lab_results")
    doctor = db.relationship("Doctor")

class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.Enum("scheduled", "completed", "canceled"), default="scheduled")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient = db.relationship("Patient", backref="appointments")
    doctor = db.relationship("Doctor")
class Recommendation(db.Model):
    __tablename__ = "recommendations"
    id          = db.Column(db.Integer, primary_key=True)
    patient_id  = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id   = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    text        = db.Column(db.Text, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", backref="recommendations")
    doctor  = db.relationship("Doctor")

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    sender = db.relationship("User", foreign_keys=[from_user_id])
    receiver = db.relationship("User", foreign_keys=[to_user_id])

class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User")
