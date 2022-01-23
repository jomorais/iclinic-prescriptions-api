from services.patientsservice import PatientsService
from model.patient import Patient
from model.error import Errors, Error, iClinicErrors


def test_patientsservice_get_patient_success():
    def setup():
        class MockedRequester:
            def get(self, url):
                return {"id": 1, "name": "Pedro Henrique Aragão", "email": "anacampos@nogueira.net", "phone": "(051) 2502-3645"}, True

        ps = PatientsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                             path="/patients/", retries=2, timeout=3, cache_ttl=43200,
                             auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGF0aWVudHMifQ.Pr6Z58GzNRtjX8Y09hEBzl7dluxsGiaxGlfzdaphzVU")
        ps.requester = MockedRequester()
        return ps

    ps = setup()
    response, status = ps.get_patient(1)
    assert status
    assert type(response) == Patient
    assert response.id == 1
    assert response.name == "Pedro Henrique Aragão"
    assert response.email == "anacampos@nogueira.net"
    assert response.phone == "(051) 2502-3645"


def test_patientsservice_get_patient_not_found():
    def setup():
        class MockedRequester:
            def get(self, url):
                return Errors.HTTP_STATUS.build_json(code=404), False

        ps = PatientsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                             path="/patients/", retries=2, timeout=3, cache_ttl=43200,
                             auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGF0aWVudHMifQ.Pr6Z58GzNRtjX8Y09hEBzl7dluxsGiaxGlfzdaphzVU")
        ps.requester = MockedRequester()
        return ps

    cs = setup()
    response, status = cs.get_patient(51)
    assert not status
    assert type(response) == Error
    assert response.message == iClinicErrors.PATIENT_NOT_FOUND.message
    assert response.code == iClinicErrors.PATIENT_NOT_FOUND.code


def test_patientsservice_get_patient_service_not_available():
    def setup():
        class MockedRequester:
            def get(self, url):
                return Errors.HTTP_STATUS.build_json(code=503), False

        ps = PatientsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                             path="/patients/", retries=2, timeout=3, cache_ttl=43200,
                             auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGF0aWVudHMifQ.Pr6Z58GzNRtjX8Y09hEBzl7dluxsGiaxGlfzdaphzVU")
        ps.requester = MockedRequester()
        return ps
    ps = setup()
    response, status = ps.get_patient(1)
    assert not status
    assert type(response) == Error
    assert response.message == iClinicErrors.PATIENTS_SERVICE_NOT_AVAILABLE.message
    assert response.code == iClinicErrors.PATIENTS_SERVICE_NOT_AVAILABLE.code

