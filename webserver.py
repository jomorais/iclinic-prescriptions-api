from flask import Flask, request, render_template

from database.database import IClinicDatabase
from api.prescriptions import Prescriptions


app = Flask(__name__)

api = Prescriptions(database=IClinicDatabase())


@app.route('/')
def home():
    return "Prescriptions REST API"


@app.route('/prescriptions', methods=["POST"])
def prescriptions():
    return api.build_prescription(request.json)


app.run(host='localhost', port=8001)

