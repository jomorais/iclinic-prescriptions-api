from services.clinicsservice import ClinicsService
from services.patientsservice import PatientsService
from services.physiciansservice import PhysiciansService
from services.metricsservice import MetricsService
from model.prescription import Prescription
from model.metric import Metric
from utils.tools import validate_json
from model.error import Errors
from database.database import DatabaseStatus
from model.http import HttpResponse
import logging


class Prescriptions:
    def __init__(self, database):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        self.database = database
        self.clinics_service = ClinicsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                                              path="/clinics/", retries=3, timeout=5, cache_ttl=259200,
                                              auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ")
        self.patients_service = PatientsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                                                path="/patients/", retries=2, timeout=3, cache_ttl=43200,
                                                auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGF0aWVudHMifQ.Pr6Z58GzNRtjX8Y09hEBzl7dluxsGiaxGlfzdaphzVU")
        self.physicians_service = PhysiciansService(host="https://mock-api-challenge.dev.iclinic.com.br",
                                                    path="/physicians/", retries=2, timeout=4, cache_ttl=172800,
                                                    auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA")
        self.metrics_service = MetricsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                                              path="/metrics/", retries=5, timeout=6, cache_ttl=0,
                                              auth_token="Bearer SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")

    def create_prescription(self, prescription_info):
        if validate_json(json_object=prescription_info, schema=Prescription.schema) is False:
            return HttpResponse(json=Errors.MALFORMED_REQUEST.build_json(), code=400)

        # collect Physician info from Physicians Service API
        physician, status = self.physicians_service.get_physician(id=prescription_info['physician']['id'])
        if not status:
            logging.error("Prescriptions.create_prescription(): physicians_service.get_physician(): %s" % physician.build_json())
            return HttpResponse(json=physician.build_json(), code=400)
        logging.info("Prescriptions.create_prescription(): Physician acquired from Physicians Service API: %s" % physician.build_json())

        # collect Patient info from Patients Service API
        patient, status = self.patients_service.get_patient(id=prescription_info['patient']['id'])
        if not status:
            logging.error("Prescriptions.create_prescription(): patients_service.get_patient(): %s" % patient.build_json())
            return HttpResponse(json=patient.build_json(), code=400)
        logging.info("Prescriptions.create_prescription(): Patient acquired from Patient Service API: %s" % patient.build_json())

        metric = Metric()
        # collect Clinic info from Clinics Service API
        clinic, status = self.clinics_service.get_clinic(id=prescription_info['clinic']['id'])
        if status:
            logging.info("Prescriptions.create_prescription(): Clinic acquired from Clinics Service API: %s" % clinic.build_json())
            metric.set_clinic(clinic)
            print(clinic)
        else:
            logging.warning("Prescriptions.create_prescription(): Clinic not found: %s" % clinic.build_json())

        metric.set_physician(physician)
        metric.set_patient(patient)
        prescription = Prescription(clinic_id=prescription_info['clinic']['id'],
                                    patient_id=patient.id,
                                    physician_id=physician.id,
                                    text=prescription_info['text'])

        logging.info("Prescriptions.create_prescription(): New Prescription: %s" % prescription.build_json())
        logging.info("Prescriptions.create_prescription(): saving in database...")

        # persist prescription and set metrics to Metrics Service API
        status, registered_prescription = self.database.register_prescription(prescription)
        if status == DatabaseStatus.REGISTER_PRESCRIPTION_ERROR:
            logging.error("Prescriptions.create_prescription(): cant save prescription to database")
            return HttpResponse(json=Errors.DATABASE_ERROR.build_json(), code=400)

        logging.info("Prescriptions.create_prescription(): SAVED! prescription.id: %s" % registered_prescription.id)

        metric.prescription_id = registered_prescription.id

        logging.info("Prescriptions.create_prescription(): New Metric: %s" % metric.build_json())
        logging.info("Prescriptions.create_prescription(): integrating it in Metrics Service API...")
        metrics, status = self.metrics_service.set_metrics(metrics=metric)
        if not status:
            # rollback
            logging.error("Prescriptions.create_prescription(): error posting Metrics in Metrics Service API!")
            logging.error("Prescriptions.create_prescription(): making rollback in prescription earlier saved")
            status, removed_prescription = self.database.remove_prescription(registered_prescription.id)
            if status == DatabaseStatus.REMOVE_PRESCRIPTION_ERROR:
                logging.error("Prescriptions.create_prescription(): cant remove prescription from database")
                return HttpResponse(json=Errors.DATABASE_ERROR.build_json(), code=400)
            logging.error("Prescriptions.create_prescription(): rollback is done")
            return HttpResponse(json=metrics.build_json(), code=400)

        logging.info("Prescriptions.create_prescription(): Metrics are integrated!! Metrics.id: %s" % metrics.id)

        logging.info("Prescriptions.create_prescription(): applying Metrics.id into prescription...")
        # update metric_id in prescription
        registered_prescription.metric_id = metrics.id
        status, new_prescription = self.database.update_prescription(registered_prescription)
        if status == DatabaseStatus.UPDATE_PRESCRIPTION_ERROR:
            logging.info("Prescriptions.create_prescription(): Metrics.id couldn't applied due DATABASE ERROR")
            return HttpResponse(json=Errors.DATABASE_ERROR.build_json(), code=400)

        logging.info("Prescriptions.create_prescription(): New Prescription are created successfully!!")
        logging.info("Prescriptions.create_prescription(): New Prescription: %s" % new_prescription.build_json())
        return HttpResponse(json=new_prescription.build_json(), code=201)


