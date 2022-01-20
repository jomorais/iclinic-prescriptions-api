from services.clinicsservice import ClinicsService
from services.patientsservice import PatientsService
from services.physiciansservice import PhysiciansService
from services.metricsservice import MetricsService
from model.prescription import Prescription
from model.metric import Metric
from utils.tools import mandatory_keys_checker
from model.error import Errors


class Prescritions:
    def __init__(self, database):
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

    def build_prescription(self, prescription_info):
        if mandatory_keys_checker(mandatory_keys=['clinic', 'physician', 'patient', 'text'],
                                  dict_object=prescription_info):
            return Errors.MALFORMED_REQUEST.build_json()

        prescription = Prescription()
        metric = Metric()

        # collect Physician info from Physicians Service API
        physician, status = self.physicians_service.get_physician(id=prescription_info['physician']['id'])
        if not status:
            return physician.build_json()
        prescription.physician_id = physician.id
        metric.physician_id = physician.id
        metric.physician_name = physician.name
        metric.physician_crm = physician.crm

        # collect Patient info from Patients Service API
        patient, status = self.patients_service.get_patient(id=prescription_info['patient']['id'])
        if not status:
            return patient.build_json()
        prescription.patient_id = patient.id
        metric.patient_id = patient.id
        metric.patient_name = patient.name
        metric.patient_email = patient.email
        metric.patient_phone = patient.phone

        # collect Clinic info from Clinics Service API
        clinic, status = self.clinics_service.get_clinic(id=prescription_info['clinic']['id'])
        if status:
            prescription.clinic_id = clinic.id
            metric.clinic_id = clinic.id
            metric.clinic_name = clinic.name

        prescription_id, status = self.database.save_prescription(prescription)
        if not status:
            return Errors.DATABASE_ERROR.build_json()

        # persist prescription and set metrics to Metrics Service API
        metric.prescription_id = prescription_id
        metrics, status = self.metrics_service.set_metrics(metrics=metric)
        if not status:
            # rollback
            if self.database.delete_prescription(prescription_id) is False:
                return Errors.DATABASE_ERROR.build_json()
            return metrics.build_json()

        # update metric_id in prescription
        prescription.metric_id = metric.id
        self.database.update_prescription(prescription)
        if not status:
            return Errors.DATABASE_ERROR.build_json()

        return prescription.build_json()
