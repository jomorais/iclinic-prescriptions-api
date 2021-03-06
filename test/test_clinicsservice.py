from services.clinicsservice import ClinicsService
from model.clinic import Clinic
from model.error import Errors, Error, iClinicErrors


def test_clinicservice_get_clinic_success():
    def setup():
        class MockedRequester:
            def get(self, url):
                return {"id": 1, "name": "Lopes"}, True

        cs = ClinicsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                              path="/clinics/", retries=3, timeout=5, cache_ttl=259200,
                              auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ")
        cs.requester = MockedRequester()
        return cs

    cs = setup()
    response, status = cs.get_clinic(1)
    assert status
    assert type(response) == Clinic


def test_clinicservice_get_clinic_not_found():
    def setup():
        class MockedRequester:
            def get(self, url):
                return Errors.HTTP_STATUS.build_json(code=404), False

        cs = ClinicsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                            path="/clinics/", retries=3, timeout=5, cache_ttl=259200,
                            auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ")
        cs.requester = MockedRequester()
        return cs

    cs = setup()
    response, status = cs.get_clinic(51)
    assert not status
    assert type(response) == Error
    assert response.message == iClinicErrors.CLINIC_NOT_FOUND.message
    assert response.code == iClinicErrors.CLINIC_NOT_FOUND.code


def test_clinicservice_get_clinic_service_not_available():
    def setup():
        class MockedRequester:
            def get(self, url):
                return Errors.HTTP_STATUS.build_json(code=503), False

        cs = ClinicsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                            path="/clinics/", retries=3, timeout=5, cache_ttl=259200,
                            auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ")
        cs.requester = MockedRequester()
        return cs
    cs = setup()
    response, status = cs.get_clinic(1)
    assert not status
    assert type(response) == Error
    assert response.message == iClinicErrors.CLINICS_SERVICE_NOT_AVAILABLE.message
    assert response.code == iClinicErrors.CLINICS_SERVICE_NOT_AVAILABLE.code


def test_clinicservice_get_clinic_http_status():
    def setup():
        class MockedRequester:
            def get(self, url):
                return Errors.HTTP_STATUS.build_json(code=203), False

        cs = ClinicsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                            path="/clinics/", retries=3, timeout=5, cache_ttl=259200,
                            auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ")
        cs.requester = MockedRequester()
        return cs
    cs = setup()
    response, status = cs.get_clinic(1)
    assert not status
    assert type(response) == Error
    assert response.message == Errors.HTTP_STATUS.message
    assert response.code == Errors.HTTP_STATUS.code


def test_clinicservice_get_clinic_invalid_clinics_service_response():
    def setup():
        class MockedRequester:
            def get(self, url):
                return {"id": "1", "name": "liliane"}, True

        cs = ClinicsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                            path="/clinics/", retries=3, timeout=5, cache_ttl=259200,
                            auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ")
        cs.requester = MockedRequester()
        return cs
    cs = setup()
    response, status = cs.get_clinic(1)
    assert not status
    assert type(response) == Error
    assert response.message == iClinicErrors.INVALID_CLINICS_SERVICE_RESPONSE.message
    assert response.code == iClinicErrors.INVALID_CLINICS_SERVICE_RESPONSE.code
