from services.dependentservice import DependentService
from model.physician import Physician
from model.error import Errors


class PhysiciansService(DependentService):
    def __init__(self, host, path, auth_token, timeout, retries, cache_ttl):
        super().__init__(host, auth_token, timeout, retries, cache_ttl)
        self.path = path

    def get_physician(self, id):
        service_url = "%s%s%s/" % (self.host, self.path, id)
        response, status = self.get(url=service_url)
        if status:
            return Physician(id=response["id"], name=response["name"], crm=response["crm"]), True
        if response["error"]["code"] == 404:
            return Errors.PHYSICIAN_NOT_FOUND, False
        if response["error"]["code"] == 503:
            return Errors.PHYSICIANS_SERVICE_NOT_AVAILABLE, False

