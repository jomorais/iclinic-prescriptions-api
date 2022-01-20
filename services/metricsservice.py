from services.dependentservice import DependentService
from model.metric import Metric
from model.error import Errors


class MetricsService(DependentService):
    def __init__(self, host, path, auth_token, timeout, retries, cache_ttl):
        super().__init__(host, auth_token, timeout, retries, cache_ttl)
        self.path = path

    def set_metrics(self, metrics):
        service_url = "%s%s%s/" % (self.host, self.path, id)
        response, status = self.post(url=service_url, content=metrics)
        if status:
            return Metric(id=response["id"],
                          clinic_id=response["clinic_id"],
                          clinic_name=response["clinic_name"],
                          physician_id=response["physician_id"],
                          physician_name=response["physician_name"],
                          physician_crm=response["physician_crm"],
                          patient_id=response["patient_id"],
                          patient_name=response["patient_name"],
                          patient_email=response["patient_email"],
                          patient_phone=response["patient_phone"],
                          prescription_id=response["prescription_id"]), True
        if response["error"]["code"] == 400:
            return Errors.MALFORMED_REQUEST, False
        if response["error"]["code"] == 503:
            return Errors.METRICS_SERVICE_NOT_AVAILABLE, False

