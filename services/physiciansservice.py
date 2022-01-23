from services.dependentservice import DependentService
from model.physician import Physician
from model.error import Errors, iClinicErrors
from utils.tools import validate_json


class PhysiciansService(DependentService):
    def __init__(self, host, path, auth_token, timeout, retries, cache_ttl):
        super().__init__(host, auth_token, timeout, retries, cache_ttl)
        self.path = path

    def get_physician(self, physician_id):
        service_url = "%s%s%s/" % (self.host, self.path, physician_id)
        response, status = self.get(url=service_url)
        if not status:
            if response["error"]["code"] == 404:
                return iClinicErrors.PHYSICIAN_NOT_FOUND, False
            if response["error"]["code"] == 503:
                return iClinicErrors.PHYSICIANS_SERVICE_NOT_AVAILABLE, False
            Errors.HTTP_STATUS.code = response["error"]["code"]
            Errors.HTTP_STATUS.http_code = Errors.HTTP_STATUS.code
            Errors.HTTP_STATUS.message = response["error"]["message"]
            return Errors.HTTP_STATUS, False
        if validate_json(json_object=response, schema=Physician.schema) is False:
            return iClinicErrors.INVALID_PHYSICIANS_SERVICE_RESPONSE, False
        return Physician(id=response["id"], name=response["name"], crm=response["crm"]), True


