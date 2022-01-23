from services.physiciansservice import PhysiciansService
from model.physician import Physician
from model.error import Errors, Error, iClinicErrors


def test_physiciansservice_get_physician_success():
    def setup():
        class MockedRequester:
            def get(self, url):
                return {"id": 1, "name": "Evelyn da Rosa", "crm": "75423070"}, True

        ps = PhysiciansService(host="https://mock-api-challenge.dev.iclinic.com.br",
                               path="/physicians/", retries=2, timeout=4, cache_ttl=172800,
                               auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA")
        ps.requester = MockedRequester()
        return ps

    ps = setup()
    response, status = ps.get_physician(1)
    assert status
    assert type(response) == Physician


def test_physiciansservice_get_physician_not_found():
    def setup():
        class MockedRequester:
            def get(self, url):
                return Errors.HTTP_STATUS.build_json(code=404), False

        ps = PhysiciansService(host="https://mock-api-challenge.dev.iclinic.com.br",
                               path="/physicians/", retries=2, timeout=4, cache_ttl=172800,
                               auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA")
        ps.requester = MockedRequester()
        return ps

    cs = setup()
    response, status = cs.get_physician(51)
    assert not status
    assert type(response) == Error
    assert response.message == iClinicErrors.PHYSICIAN_NOT_FOUND.message
    assert response.code == iClinicErrors.PHYSICIAN_NOT_FOUND.code


def test_physiciansservice_get_physician_service_not_available():
    def setup():
        class MockedRequester:
            def get(self, url):
                return Errors.HTTP_STATUS.build_json(code=503), False

        ps = PhysiciansService(host="https://mock-api-challenge.dev.iclinic.com.br",
                               path="/physicians/", retries=3, timeout=5, cache_ttl=259200,
                               auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ")
        ps.requester = MockedRequester()
        return ps
    ps = setup()
    response, status = ps.get_physician(1)
    assert not status
    assert type(response) == Error
    assert response.message == iClinicErrors.PHYSICIANS_SERVICE_NOT_AVAILABLE.message
    assert response.code == iClinicErrors.PHYSICIANS_SERVICE_NOT_AVAILABLE.code

