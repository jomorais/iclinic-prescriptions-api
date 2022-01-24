from services.metricsservice import MetricsService
from model.metric import Metric
from model.error import Errors, Error, iClinicErrors


def test_metricsservice_set_metrics_success():
    def setup():
        metrics = Metric(clinic_id=1,
                         clinic_name="Clinica A",
                         physician_id=1,
                         physician_name="José",
                         physician_crm="SP293893",
                         patient_id=1,
                         patient_name="Rodrigo",
                         patient_email="rodrigo@gmail.com",
                         patient_phone="(16)998765625",
                         prescription_id=1)

        class MockedRequester:
            def post(self, url, content):
                return metrics.build_json(), True

        ms = MetricsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                            path="/metrics/", retries=5, timeout=6, cache_ttl=0,
                            auth_token="Bearer SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
        ms.requester = MockedRequester()
        return metrics, ms

    metrics, ms = setup()
    response, status = ms.set_metrics(metrics=metrics)
    assert status
    assert type(response) == Metric
    assert response.id == ""
    assert response.clinic_id == 1
    assert response.clinic_name == "Clinica A"
    assert response.physician_id == 1
    assert response.physician_name == "José"
    assert response.physician_crm == "SP293893"
    assert response.patient_id == 1
    assert response.patient_name == "Rodrigo"
    assert response.patient_email == "rodrigo@gmail.com"
    assert response.patient_phone == "(16)998765625"
    assert response.prescription_id == 1


def test_metricsservice_set_metrics_malformed_request():
    def setup():
        metrics = Metric(clinic_id=1,
                         clinic_name="Clinica A",
                         physician_id=1,
                         physician_name="José",
                         physician_crm="SP293893",
                         patient_id=1,
                         patient_name="Rodrigo",
                         patient_email="rodrigo@gmail.com",
                         patient_phone="(16)998765625",
                         prescription_id=1)

        class MockedRequester:
            def post(self, url, content):
                return Errors.HTTP_STATUS.build_json(code=400), False

        ms = MetricsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                            path="/metrics/", retries=5, timeout=6, cache_ttl=0,
                            auth_token="Bearer SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
        ms.requester = MockedRequester()
        return metrics, ms

    metrics, ms = setup()
    response, status = ms.set_metrics(metrics=metrics)
    assert not status
    assert type(response) == Error
    assert response.message == Errors.MALFORMED_REQUEST.message
    assert response.code == Errors.MALFORMED_REQUEST.code


def test_metricsservice_set_metrics_service_not_available():
    def setup():
        metrics = Metric(clinic_id=1,
                         clinic_name="Clinica A",
                         physician_id=1,
                         physician_name="José",
                         physician_crm="SP293893",
                         patient_id=1,
                         patient_name="Rodrigo",
                         patient_email="rodrigo@gmail.com",
                         patient_phone="(16)998765625",
                         prescription_id=1)

        class MockedRequester:
            def post(self, url, content):
                return Errors.HTTP_STATUS.build_json(code=503), False

        ms = MetricsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                            path="/metrics/", retries=5, timeout=6, cache_ttl=0,
                            auth_token="Bearer SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
        ms.requester = MockedRequester()
        return metrics, ms
    metrics, ms = setup()
    response, status = ms.set_metrics(metrics=metrics)
    assert not status
    assert type(response) == Error
    assert response.message == iClinicErrors.METRICS_SERVICE_NOT_AVAILABLE.message
    assert response.code == iClinicErrors.METRICS_SERVICE_NOT_AVAILABLE.code


def test_metricsservice_set_metrics_http_status():
    def setup():
        metrics = Metric(clinic_id=1,
                         clinic_name="Clinica A",
                         physician_id=1,
                         physician_name="José",
                         physician_crm="SP293893",
                         patient_id=1,
                         patient_name="Rodrigo",
                         patient_email="rodrigo@gmail.com",
                         patient_phone="(16)998765625",
                         prescription_id=1)

        class MockedRequester:
            def post(self, url, content):
                return Errors.HTTP_STATUS.build_json(code=203), False

        ms = MetricsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                            path="/metrics/", retries=5, timeout=6, cache_ttl=0,
                            auth_token="Bearer SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
        ms.requester = MockedRequester()
        return metrics, ms
    metrics, ms = setup()
    response, status = ms.set_metrics(metrics=metrics)
    assert not status
    assert type(response) == Error
    assert response.message == Errors.HTTP_STATUS.message
    assert response.code == Errors.HTTP_STATUS.code


def test_metricsservice_set_metrics_validate_json():
    def setup():
        metrics = Metric(clinic_id=1,
                         clinic_name="Clinica A",
                         physician_id=1,
                         physician_name="José",
                         physician_crm="SP293893",
                         patient_id=1,
                         patient_name="Rodrigo",
                         patient_email="rodrigo@gmail.com",
                         patient_phone="(16)998765625",
                         prescription_id=1)

        class MockedRequester:
            def post(self, url, content):
                return {"id": 123}, True

        ms = MetricsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                            path="/metrics/", retries=5, timeout=6, cache_ttl=0,
                            auth_token="Bearer SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
        ms.requester = MockedRequester()
        return metrics, ms
    metrics, ms = setup()
    response, status = ms.set_metrics(metrics=metrics)
    assert not status
    assert type(response) == Error
    assert response.message == iClinicErrors.INVALID_METRICS_SERVICE_RESPONSE.message
    assert response.code == iClinicErrors.INVALID_METRICS_SERVICE_RESPONSE.code


def test_metricsservice_set_metrics_metrics_without_clinic_info():
    def setup():
        metrics = Metric(physician_id=1,
                         physician_name="José",
                         physician_crm="SP293893",
                         patient_id=1,
                         patient_name="Rodrigo",
                         patient_email="rodrigo@gmail.com",
                         patient_phone="(16)998765625",
                         prescription_id=1)

        class MockedRequester:
            def post(self, url, content):
                return metrics.build_json(), True

        ms = MetricsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                            path="/metrics/", retries=5, timeout=6, cache_ttl=0,
                            auth_token="Bearer SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
        ms.requester = MockedRequester()
        return metrics, ms
    metrics, ms = setup()
    response, status = ms.set_metrics(metrics=metrics)
    assert status
    assert "clinic_id" not in metrics.build_json()
    assert "clinic_name" not in metrics.build_json()



