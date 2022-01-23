from services.dependentservice import DependentService
from model.clinic import Clinic
from model.error import Errors, iClinicErrors
from utils.tools import validate_json


class ClinicsService(DependentService):
    def __init__(self, host, path, auth_token, timeout, retries, cache_ttl):
        super().__init__(host, auth_token, timeout, retries, cache_ttl)
        self.path = path

    def get_clinic(self, clinic_id: int):
        service_url = "%s%s%s/" % (self.host, self.path, clinic_id)
        response, status = self.get(url=service_url)
        if not status:
            if response["error"]["code"] == 404:
                return iClinicErrors.CLINIC_NOT_FOUND, False
            if response["error"]["code"] == 503:
                return iClinicErrors.CLINICS_SERVICE_NOT_AVAILABLE, False
            Errors.HTTP_STATUS.code = response["error"]["code"]
            Errors.HTTP_STATUS.http_code = Errors.HTTP_STATUS.code
            Errors.HTTP_STATUS.message = response["error"]["message"]
            return Errors.HTTP_STATUS, False
        if validate_json(json_object=response, schema=Clinic.schema) is False:
            return iClinicErrors.INVALID_CLINICS_SERVICE_RESPONSE, False
        return Clinic(id=response["id"], name=response["name"]), True
