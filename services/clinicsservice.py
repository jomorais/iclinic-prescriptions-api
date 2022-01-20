from services.dependentservice import DependentService
from model.clinic import Clinic
from model.error import Errors


class ClinicsService(DependentService):
    def __init__(self, host, path, auth_token, timeout, retries, cache_ttl):
        super().__init__(host, auth_token, timeout, retries, cache_ttl)
        self.path = path

    def get_clinic(self, id):
        service_url = "%s%s%s/" % (self.host, self.path, id)
        response, status = self.get(url=service_url)
        if status:
            return Clinic(id=response["id"], name=response["name"]), True
        if response["error"]["code"] == 404:
            return Errors.CLINIC_NOT_FOUND, False
        if response["error"]["code"] == 503:
            return Errors.CLINICS_SERVICE_NOT_AVAILABLE, False

