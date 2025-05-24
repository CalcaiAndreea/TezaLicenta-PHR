from flask import Flask
from dotenv import load_dotenv
from config import Config
from db import db 

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

import models  # noqa: F401 (tabelele)

# Blueprint-uri
from login import login_bp;                  app.register_blueprint(login_bp)
from patient_dashboard import patient_bp;    app.register_blueprint(patient_bp)
from doctor_dashboard import doctor_bp;  app.register_blueprint(doctor_bp)
# app.py  (după celelalte imports)
from messaging import messaging_bp;  app.register_blueprint(messaging_bp)
from recommendations import recommend_bp; app.register_blueprint(recommend_bp)

#from view_patient import view_patient_bp;   app.register_blueprint(view_patient_bp)
from add_vital import add_vital_bp;          app.register_blueprint(add_vital_bp)
from add_allergy import add_allergy_bp;      app.register_blueprint(add_allergy_bp)
from list_vitals import list_vitals_bp;      app.register_blueprint(list_vitals_bp)
from list_allergies import list_allergies_bp;app.register_blueprint(list_allergies_bp)

@app.route("/")
def home():
    return "<h3>PHR Prototype live – <a href='/login'>Login</a></h3>"

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)




