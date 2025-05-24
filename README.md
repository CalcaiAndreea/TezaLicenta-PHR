# 🩺 TezaLicenta-PHR

Un prototip de aplicație pentru gestionarea datelor medicale personale (PHR) și facilitarea interacțiunii dintre pacient și medic. Include un sistem inteligent de recomandări medicale bazat pe date clinice și analize de laborator.

## 📌 Funcționalități principale

- Autentificare separată pentru pacient și medic
- Adăugare și vizualizare date PHR (simptome, analize, alergii, valori vitale)
- Trimiterea mesajelor între pacient și medic
- Recomandări generate de un model AI pe baza datelor introduse
- Vizualizare recomandări și opțiune de aprobare/editare de către medic

## 🧠 Tehnologii folosite

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS (Jinja2 templates)
- **Bază de date:** SQLite
- **Machine Learning:** Scikit-learn
- **Altele:** Git, Jinja2, Flask-SQLAlchemy

## 📂 Structura proiectului

| Folder / Fișier | Descriere |
|-----------------|-----------|
| `app.py` | Punctul de pornire al aplicației Flask |
| `models.py` | Modelele bazei de date (Pacient, Medic, Analize etc.) |
| `config.py`, `db.py` | Configurarea și inițializarea bazei de date |
| `templates/` | Șabloanele HTML (folosind Jinja2) |
| `static/css/` | Fișierele CSS pentru interfață |
| `patient_dashboard.py` | Funcționalitățile pentru interfața pacientului |
| `doctor_dashboard.py` | Funcționalitățile pentru medic |
| `recommendations.py` | Modulul AI care generează recomandări medicale |
| `messaging.py` | Sistem de mesagerie între pacient și medic |
| `add_allergy.py`, `add_vital.py` | Formulare pentru introducerea de date |
| `login.py`, `logout.py` | Autentificare și deconectare utilizatori |
| `list_allergies.py`, `list_vitals.py` | Vizualizarea listelor de date PHR |
| `view_patient.py` | Modul pentru medic de a accesa fișa pacientului |
| `.env` | Variabile de mediu (ascuns în mod normal) |
