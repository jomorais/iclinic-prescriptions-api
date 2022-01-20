from services.dependentservice import DependentService
from model.patient import Patient
from model.error import Errors


class PatientsService(DependentService):
    def __init__(self, host, path, auth_token, timeout, retries, cache_ttl):
        super().__init__(host, auth_token, timeout, retries, cache_ttl)
        self.path = path

    def get_patient(self, id):
        service_url = "%s%s%s/" % (self.host, self.path, id)
        response, status = self.get(url=service_url)
        if status:
            return Patient(id=response["id"], name=response["name"],
                           email=response["email"], phone=response["phone"]), True
        if response["error"]["code"] == 404:
            return Errors.PATIENT_NOT_FOUND, False
        if response["error"]["code"] == 503:
            return Errors.PATIENTS_SERVICE_NOT_AVAILABLE, False


