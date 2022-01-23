from services.dependentservice import DependentService
from model.metric import Metric
from model.error import Errors, iClinicErrors
from utils.tools import validate_json


class MetricsService(DependentService):
    def __init__(self, host, path, auth_token, timeout, retries, cache_ttl):
        super().__init__(host, auth_token, timeout, retries, cache_ttl)
        self.path = path

    def set_metrics(self, metrics: Metric):
        service_url = "%s%s" % (self.host, self.path)
        response, status = self.post(url=service_url, content=metrics.build_json())
        if not status:
            if response["error"]["code"] == 400:
                return Errors.MALFORMED_REQUEST, False
            if response["error"]["code"] == 503:
                return iClinicErrors.METRICS_SERVICE_NOT_AVAILABLE, False
            Errors.HTTP_STATUS.code = response["error"]["code"]
            Errors.HTTP_STATUS.http_code = Errors.HTTP_STATUS.code
            Errors.HTTP_STATUS.message = response["error"]["message"]
            return Errors.HTTP_STATUS, False

        if validate_json(json_object=response, schema=Metric.schema) is False:
            return iClinicErrors.INVALID_METRICS_SERVICE_RESPONSE, False

        if 'clinic_id' in response and 'clinic_name' in response:
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
                          prescription_id=metrics.prescription_id), True
        return Metric(id=response["id"],
                      physician_id=response["physician_id"],
                      physician_name=response["physician_name"],
                      physician_crm=response["physician_crm"],
                      patient_id=response["patient_id"],
                      patient_name=response["patient_name"],
                      patient_email=response["patient_email"],
                      patient_phone=response["patient_phone"],
                      prescription_id=metrics.prescription_id), True

