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
from services.settings import dependent_services_settings
import logging


class Prescriptions:
    def __init__(self, database):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        self.database = database
        self.clinics_service = ClinicsService(host=dependent_services_settings["clinics-service"]["host"],
                                              path=dependent_services_settings["clinics-service"]["path"],
                                              retries=dependent_services_settings["clinics-service"]["retries"],
                                              timeout=dependent_services_settings["clinics-service"]["timeout"],
                                              cache_ttl=dependent_services_settings["clinics-service"]["cache_ttl"],
                                              auth_token=dependent_services_settings["clinics-service"]["auth_token"])

        self.patients_service = PatientsService(host=dependent_services_settings["patients-service"]["host"],
                                                path=dependent_services_settings["patients-service"]["path"],
                                                retries=dependent_services_settings["patients-service"]["retries"],
                                                timeout=dependent_services_settings["patients-service"]["timeout"],
                                                cache_ttl=dependent_services_settings["patients-service"]["cache_ttl"],
                                                auth_token=dependent_services_settings["patients-service"]["auth_token"])

        self.physicians_service = PhysiciansService(host=dependent_services_settings["physicians-service"]["host"],
                                                    path=dependent_services_settings["physicians-service"]["path"],
                                                    retries=dependent_services_settings["physicians-service"]["retries"],
                                                    timeout=dependent_services_settings["physicians-service"]["timeout"],
                                                    cache_ttl=dependent_services_settings["physicians-service"]["cache_ttl"],
                                                    auth_token=dependent_services_settings["physicians-service"]["auth_token"])

        self.metrics_service = MetricsService(host=dependent_services_settings["metrics-service"]["host"],
                                              path=dependent_services_settings["metrics-service"]["path"],
                                              retries=dependent_services_settings["metrics-service"]["retries"],
                                              timeout=dependent_services_settings["metrics-service"]["timeout"],
                                              cache_ttl=dependent_services_settings["metrics-service"]["cache_ttl"],
                                              auth_token=dependent_services_settings["metrics-service"]["auth_token"])

    def create_prescription(self, prescription_info):
        if validate_json(json_object=prescription_info, schema=Prescription.schema) is False:
            logging.error("Prescriptions.create_prescription(): Malformed prescription_info: %s" % prescription_info)
            return HttpResponse(json=Errors.MALFORMED_REQUEST.build_json(), code=Errors.MALFORMED_REQUEST.http_code)

        logging.info("Prescriptions.create_prescription(): creating a new prescription: %s" % prescription_info)
        logging.info("Prescriptions.create_prescription(): accessing Dependent Services...")
        # collect Physician info from Physicians Service API
        physician, status = self.physicians_service.get_physician(id=prescription_info['physician']['id'])
        if not status:
            logging.error("Prescriptions.create_prescription(): physicians_service.get_physician(): %s" % physician.build_json())
            return HttpResponse(json=physician.build_json(), code=physician.http_code)
        logging.info("Prescriptions.create_prescription(): Physician acquired from Physicians Service API: %s" % physician.build_json())

        # collect Patient info from Patients Service API
        patient, status = self.patients_service.get_patient(id=prescription_info['patient']['id'])
        if not status:
            logging.error("Prescriptions.create_prescription(): patients_service.get_patient(): %s" % patient.build_json())
            return HttpResponse(json=patient.build_json(), code=patient.http_code)
        logging.info("Prescriptions.create_prescription(): Patient acquired from Patient Service API: %s" % patient.build_json())

        metric = Metric()
        # collect Clinic info from Clinics Service API
        clinic, status = self.clinics_service.get_clinic(id=prescription_info['clinic']['id'])
        if status:
            logging.info("Prescriptions.create_prescription(): Clinic acquired from Clinics Service API: %s" % clinic.build_json())
            metric.set_clinic(clinic)
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
            return HttpResponse(json=Errors.DATABASE_ERROR.build_json(), code=Errors.DATABASE_ERROR.http_code)

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
                return HttpResponse(json=Errors.DATABASE_ERROR.build_json(), code=Errors.DATABASE_ERROR.http_code)
            logging.error("Prescriptions.create_prescription(): rollback is done")
            return HttpResponse(json=metrics.build_json(), code=metrics.http_code)

        logging.info("Prescriptions.create_prescription(): Metrics are integrated!! Metrics.id: %s" % metrics.id)

        logging.info("Prescriptions.create_prescription(): applying Metrics.id into prescription...")
        # update metric_id in prescription
        registered_prescription.metric_id = metrics.id
        status, new_prescription = self.database.update_prescription(registered_prescription)
        if status == DatabaseStatus.UPDATE_PRESCRIPTION_ERROR:
            logging.info("Prescriptions.create_prescription(): Metrics.id couldn't applied due DATABASE ERROR")
            return HttpResponse(json=Errors.DATABASE_ERROR.build_json(), code=Errors.DATABASE_ERROR.http_code)

        logging.info("Prescriptions.create_prescription(): New Prescription are created successfully!!")
        logging.info("Prescriptions.create_prescription(): New Prescription: %s" % new_prescription.build_json())
        return HttpResponse(json=new_prescription.build_json(), code=201)


