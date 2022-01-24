from model.metric import Metric
from model.clinic import Clinic
from model.physician import Physician
from model.patient import Patient
from model.prescription import Prescription


def test_clinic():
    def setup():
        return Clinic(id=25, name="Francisco")

    clinic = setup()
    assert clinic.id == 25
    assert clinic.name == "Francisco"
    assert clinic.build_json() == {"id": 25, "name": "Francisco"}


def test_physician():
    def setup():
        return Physician(id=25, name="Ilsa", crm="321654987")

    physician = setup()
    assert physician.id == 25
    assert physician.name == "Ilsa"
    assert physician.crm == "321654987"
    assert physician.build_json() == {"id": 25, "name": "Ilsa", "crm": "321654987"}


def test_patient():
    def setup():
        return Patient(id=25, name="Liliane", email="lili@gmail.com", phone="(092) 00000-0000")

    patient = setup()
    assert patient.id == 25
    assert patient.name == "Liliane"
    assert patient.email == "lili@gmail.com"
    assert patient.phone == "(092) 00000-0000"
    assert patient.build_json() == {"id": 25, "name": "Liliane", "email": "lili@gmail.com", "phone": "(092) 00000-0000"}


def test_prescription():
    def setup():
        return Prescription(id=25, clinic_id=1, physician_id=2, patient_id=3,
                            text="Paracetamol(850mg) um(1) comprimido a cada 6h", metric_id="123")

    prescription = setup()
    assert prescription.id == 25
    assert prescription.clinic_id == 1
    assert prescription.physician_id == 2
    assert prescription.patient_id == 3
    assert prescription.text == "Paracetamol(850mg) um(1) comprimido a cada 6h"
    assert prescription.metric_id == "123"
    assert prescription.build_json() == {"data": {"id": 25,
                                                  "clinic": {"id": 1},
                                                  "physician": {"id": 2},
                                                  "patient": {"id": 3},
                                                  "text": "Paracetamol(850mg) um(1) comprimido a cada 6h",
                                                  "metric": {"id": "123"}}}


def test_metric():
    def setup():
        return Metric(id="123",
                      patient_id=1,
                      patient_name="Joao",
                      patient_email="joao@gmail.comm",
                      patient_phone="92 00000-0000",
                      clinic_id=2,
                      clinic_name="Clinica 1",
                      physician_id=3,
                      physician_name="Raimundo",
                      physician_crm="123456789",
                      prescription_id=12)

    metric = setup()
    assert metric.id == "123"
    assert metric.patient_id == 1
    assert metric.patient_name == "Joao"
    assert metric.patient_email == "joao@gmail.comm"
    assert metric.patient_phone == "92 00000-0000"
    assert metric.clinic_id == 2
    assert metric.clinic_name == "Clinica 1"
    assert metric.physician_id == 3
    assert metric.physician_name == "Raimundo"
    assert metric.physician_crm == "123456789"
    assert metric.build_json() == {"id": "123",
                                   "patient_id": 1,
                                   "patient_name": "Joao",
                                   "patient_email": "joao@gmail.comm",
                                   "patient_phone": "92 00000-0000",
                                   "clinic_id": 2,
                                   "clinic_name": "Clinica 1",
                                   "physician_id": 3,
                                   "physician_name": "Raimundo",
                                   "physician_crm": "123456789",
                                   "prescription_id": 12}
    metric.clinic_id = 0
    assert metric.build_json() == {"id": "123",
                                   "patient_id": 1,
                                   "patient_name": "Joao",
                                   "patient_email": "joao@gmail.comm",
                                   "patient_phone": "92 00000-0000",
                                   "physician_id": 3,
                                   "physician_name": "Raimundo",
                                   "physician_crm": "123456789",
                                   "prescription_id": 12}

    metric.set_clinic(clinic=Clinic(id=234, name="ProSaude"))
    assert metric.clinic_id == 234
    assert metric.clinic_name == "ProSaude"

    metric.set_physician(physician=Physician(id=556, name="Renato Telles", crm="123456789"))
    assert metric.physician_id == 556
    assert metric.physician_name == "Renato Telles"
    assert metric.physician_crm == "123456789"

    metric.set_patient(patient=Patient(id=321, name="Gabriel", email="gsilva@gmail.com", phone="(092) 321654987"))
    assert metric.patient_id == 321
    assert metric.patient_name == "Gabriel"
    assert metric.patient_email == "gsilva@gmail.com"
    assert metric.patient_phone == "(092) 321654987"

