from flask import Flask, request, render_template

from database.database import IClinicDatabase
from api.prescriptions import Prescriptions


app = Flask(__name__)

api = Prescriptions(database=IClinicDatabase())


@app.route('/')
def home():
    return "iClinic-Python-Challenge - [Prescriptions REST API]"


@app.route('/prescriptions/', methods=["POST"])
@app.route('/prescriptions', methods=["POST"])
def prescriptions():
    response = api.create_prescription(request.json)
    return response.json, response.code


app.run(host="0.0.0.0", port=8008)

