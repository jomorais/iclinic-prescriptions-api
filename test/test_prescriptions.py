from api.prescriptions import Prescriptions
from model.http import HttpResponse
from model.error import Errors, iClinicErrors
from model.clinic import Clinic
from database.database import DatabaseStatus
from model.prescription import Prescription
from model.physician import Physician
from model.patient import Patient
from model.metric import Metric


def test_prescriptions_malformed_request():
    def setup():
        class MockediClinicDatabase:
            def __init__(self):
                self.init()

            def init(self):
                pass

        return Prescriptions(database=MockediClinicDatabase())
    prescriptions = setup()
    response = prescriptions.create_prescription(prescription_info={"id": "1"})
    assert type(response) == HttpResponse
    assert response.json == Errors.MALFORMED_REQUEST.build_json()


def test_prescriptions_get_physician_error():
    def setup():
        valid_prescription = {
                          "clinic": {
                            "id": 1
                          },
                          "physician": {
                            "id": 1
                          },
                          "patient": {
                            "id": 1
                          },
                          "text": "Dipirona 1x ao dia"
                        }

        class MockediClinicDatabase:
            def __init__(self):
                self.init()

            def init(self):
                pass

        class MockediPhysiciansService:
            def get_physician(self, physician_id):
                return Errors.HTTP_ERROR, False

        p = Prescriptions(database=MockediClinicDatabase())
        p.physicians_service = MockediPhysiciansService()
        return p, valid_prescription

    prescriptions, valid_prescription = setup()
    response = prescriptions.create_prescription(prescription_info=valid_prescription)
    assert type(response) == HttpResponse
    assert response.json == Errors.HTTP_ERROR.build_json()
    assert response.code == Errors.HTTP_ERROR.http_code


def test_prescriptions_get_patient_error():
    def setup():
        valid_prescription = {
                          "clinic": {
                            "id": 1
                          },
                          "physician": {
                            "id": 1
                          },
                          "patient": {
                            "id": 1
                          },
                          "text": "Dipirona 1x ao dia"
                        }

        class MockediClinicDatabase:
            def __init__(self):
                self.init()

            def init(self):
                pass

        class MockediPhysiciansService:
            def get_physician(self, physician_id):
                return Physician(), True

        class MockediPatientsService:
            def get_patient(self, patient_id):
                return Errors.HTTP_ERROR, False

        p = Prescriptions(database=MockediClinicDatabase())
        p.physicians_service = MockediPhysiciansService()
        p.patients_service = MockediPatientsService()
        return p, valid_prescription

    prescriptions, valid_prescription = setup()
    response = prescriptions.create_prescription(prescription_info=valid_prescription)
    assert type(response) == HttpResponse
    assert response.json == Errors.HTTP_ERROR.build_json()
    assert response.code == Errors.HTTP_ERROR.http_code


def test_prescriptions_register_prescription_error_with_get_clinic_info():
    def setup():
        valid_prescription = {
                          "clinic": {
                            "id": 1
                          },
                          "physician": {
                            "id": 1
                          },
                          "patient": {
                            "id": 1
                          },
                          "text": "Dipirona 1x ao dia"
                        }

        class MockediClinicDatabase:
            def __init__(self):
                self.init()

            def init(self):
                pass

            def register_prescription(self, prescripttion):
                return DatabaseStatus.REGISTER_PRESCRIPTION_ERROR, None

        class MockedPhysiciansService:
            def get_physician(self, physician_id):
                return Physician(), True

        class MockedPatientsService:
            def get_patient(self, patient_id):
                return Patient(), True

        class MockedClinicsService:
            def get_clinic(self, clinic_id):
                return Clinic(id=1, name="Clinica X"), True

        p = Prescriptions(database=MockediClinicDatabase())
        p.physicians_service = MockedPhysiciansService()
        p.patients_service = MockedPatientsService()
        p.clinics_service = MockedClinicsService()
        return p, valid_prescription

    prescriptions, valid_prescription = setup()
    response = prescriptions.create_prescription(prescription_info=valid_prescription)
    assert type(response) == HttpResponse
    assert response.json == Errors.DATABASE_ERROR.build_json()
    assert response.code == Errors.DATABASE_ERROR.http_code


def test_prescriptions_register_prescription_error_without_get_clinic_info():
    def setup():
        valid_prescription = {
                          "clinic": {
                            "id": 1
                          },
                          "physician": {
                            "id": 1
                          },
                          "patient": {
                            "id": 1
                          },
                          "text": "Dipirona 1x ao dia"
                        }

        class MockediClinicDatabase:
            def __init__(self):
                self.init()

            def init(self):
                pass

            def register_prescription(self, prescripttion):
                return DatabaseStatus.REGISTER_PRESCRIPTION_ERROR, None

        class MockedPhysiciansService:
            def get_physician(self, physician_id):
                return Physician(), True

        class MockedPatientsService:
            def get_patient(self, patient_id):
                return Patient(), True

        class MockedClinicsService:
            def get_clinic(self, clinic_id):
                return Errors.HTTP_ERROR, False

        p = Prescriptions(database=MockediClinicDatabase())
        p.physicians_service = MockedPhysiciansService()
        p.patients_service = MockedPatientsService()
        p.clinics_service = MockedClinicsService()

        return p, valid_prescription

    prescriptions, valid_prescription = setup()
    response = prescriptions.create_prescription(prescription_info=valid_prescription)
    assert type(response) == HttpResponse
    assert response.json == Errors.DATABASE_ERROR.build_json()
    assert response.code == Errors.DATABASE_ERROR.http_code


def test_prescriptions_set_metrics_and_remove_prescription_error():
    def setup():
        valid_prescription = {
                          "clinic": {
                            "id": 1
                          },
                          "physician": {
                            "id": 1
                          },
                          "patient": {
                            "id": 1
                          },
                          "text": "Dipirona 1x ao dia"
                        }

        class MockedClinicDatabase:
            def __init__(self):
                self.init()

            def init(self):
                pass

            def register_prescription(self, prescription):
                return DatabaseStatus.REGISTER_PRESCRIPTION_SUCCESS, Prescription()

            def remove_prescription(self, prescription):
                return DatabaseStatus.REMOVE_PRESCRIPTION_ERROR, None

        class MockedPhysiciansService:
            def get_physician(self, physician_id):
                return Physician(), True

        class MockedPatientsService:
            def get_patient(self, patient_id):
                return Patient(), True

        class MockedClinicsService:
            def get_clinic(self, clinic_id):
                return Clinic(), True

        class MockedMetricsService:
            def set_metrics(self, metrics):
                return Errors.HTTP_ERROR, False

        p = Prescriptions(database=MockedClinicDatabase())
        p.physicians_service = MockedPhysiciansService()
        p.patients_service = MockedPatientsService()
        p.clinics_service = MockedClinicsService()
        p.metrics_service = MockedMetricsService()
        return p, valid_prescription

    prescriptions, valid_prescription = setup()
    response = prescriptions.create_prescription(prescription_info=valid_prescription)
    assert type(response) == HttpResponse
    assert response.json == Errors.DATABASE_ERROR.build_json()
    assert response.code == Errors.DATABASE_ERROR.http_code


def test_prescriptions_set_metrics_error():
    def setup():
        valid_prescription = {
                          "clinic": {
                            "id": 1
                          },
                          "physician": {
                            "id": 1
                          },
                          "patient": {
                            "id": 1
                          },
                          "text": "Dipirona 1x ao dia"
                        }

        class MockedClinicDatabase:
            def __init__(self):
                self.init()

            def init(self):
                pass

            def register_prescription(self, prescription):
                return DatabaseStatus.REGISTER_PRESCRIPTION_SUCCESS, Prescription()

            def remove_prescription(self, prescription):
                return DatabaseStatus.REMOVE_PRESCRIPTION_SUCCESS, Prescription()

        class MockedPhysiciansService:
            def get_physician(self, physician_id):
                return Physician(), True

        class MockedPatientsService:
            def get_patient(self, patient_id):
                return Patient(), True

        class MockedClinicsService:
            def get_clinic(self, clinic_id):
                return Clinic(), True

        class MockedMetricsService:
            def set_metrics(self, metrics):
                return Errors.HTTP_ERROR, False

        p = Prescriptions(database=MockedClinicDatabase())
        p.physicians_service = MockedPhysiciansService()
        p.patients_service = MockedPatientsService()
        p.clinics_service = MockedClinicsService()
        p.metrics_service = MockedMetricsService()
        return p, valid_prescription

    prescriptions, valid_prescription = setup()
    response = prescriptions.create_prescription(prescription_info=valid_prescription)
    assert type(response) == HttpResponse
    assert response.json == Errors.HTTP_ERROR.build_json()
    assert response.code == Errors.HTTP_ERROR.http_code


def test_prescriptions_update_prescription_error():
    def setup():
        valid_prescription = {
                          "clinic": {
                            "id": 1
                          },
                          "physician": {
                            "id": 1
                          },
                          "patient": {
                            "id": 1
                          },
                          "text": "Dipirona 1x ao dia"
                        }

        class MockedClinicDatabase:
            def __init__(self):
                self.init()

            def init(self):
                pass

            def register_prescription(self, prescription):
                return DatabaseStatus.REGISTER_PRESCRIPTION_SUCCESS, Prescription()

            def update_prescription(self, prescription):
                return DatabaseStatus.UPDATE_PRESCRIPTION_ERROR, None

        class MockedPhysiciansService:
            def get_physician(self, physician_id):
                return Physician(), True

        class MockedPatientsService:
            def get_patient(self, patient_id):
                return Patient(), True

        class MockedClinicsService:
            def get_clinic(self, clinic_id):
                return Clinic(), True

        class MockedMetricsService:
            def set_metrics(self, metrics):
                return Metric(), True

        p = Prescriptions(database=MockedClinicDatabase())
        p.physicians_service = MockedPhysiciansService()
        p.patients_service = MockedPatientsService()
        p.clinics_service = MockedClinicsService()
        p.metrics_service = MockedMetricsService()
        return p, valid_prescription

    prescriptions, valid_prescription = setup()
    response = prescriptions.create_prescription(prescription_info=valid_prescription)
    assert type(response) == HttpResponse
    assert response.json == Errors.DATABASE_ERROR.build_json()
    assert response.code == Errors.DATABASE_ERROR.http_code


def test_prescriptions_create_prescription_success():
    def setup():
        valid_prescription = {
                          "clinic": {
                            "id": 1
                          },
                          "physician": {
                            "id": 1
                          },
                          "patient": {
                            "id": 1
                          },
                          "text": "Dipirona 1x ao dia"
                        }

        class MockedClinicDatabase:
            def __init__(self):
                self.init()

            def init(self):
                pass

            def register_prescription(self, prescription):
                return DatabaseStatus.REGISTER_PRESCRIPTION_SUCCESS, Prescription()

            def update_prescription(self, prescription):
                return DatabaseStatus.UPDATE_PRESCRIPTION_SUCCESS, Prescription()

        class MockedPhysiciansService:
            def get_physician(self, physician_id):
                return Physician(), True

        class MockedPatientsService:
            def get_patient(self, patient_id):
                return Patient(), True

        class MockedClinicsService:
            def get_clinic(self, clinic_id):
                return Clinic(), True

        class MockedMetricsService:
            def set_metrics(self, metrics):
                return Metric(), True

        p = Prescriptions(database=MockedClinicDatabase())
        p.physicians_service = MockedPhysiciansService()
        p.patients_service = MockedPatientsService()
        p.clinics_service = MockedClinicsService()
        p.metrics_service = MockedMetricsService()
        return p, valid_prescription

    prescriptions, valid_prescription = setup()
    response = prescriptions.create_prescription(prescription_info=valid_prescription)
    assert type(response) == HttpResponse
    assert response.json == Prescription().build_json()
    assert response.code == 201
