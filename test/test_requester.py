import requests.exceptions
import requests_cache

from utils.requester import Requester
from utils.error import Errors


def test_requester_non_cached_session():
    def setup():
        return Requester(auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA",
                         retries=2,
                         timeout=4,
                         cache_ttl=0)
    requester = setup()

    assert type(requester.session) != requests_cache.CachedSession


def test_requester_cached_session():
    def setup():
        return Requester(auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA",
                         retries=2,
                         timeout=4,
                         cache_ttl=172800)
    requester = setup()

    assert type(requester.session) == requests_cache.CachedSession


def test_requester_get_success():
    class MockedHttpSession:
        def get(self, url, timeout, headers):

            class Response:
                status_code = 200

                def json(self):
                    return {'id': 1, 'name': 'Evelyn da Rosa', 'crm': '75423070'}

            return Response()

    def setup():
        return Requester(auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA",
                         retries=2,
                         timeout=4,
                         cache_ttl=172800, session=MockedHttpSession())
    requester = setup()

    resp = requester.get(url="https://mock-api-challenge.dev.iclinic.com.br/physicians/1/")
    assert type(resp) == dict
    assert 'crm' in resp
    assert 'id' in resp
    assert 'name' in resp


def test_requester_get_timeout():
    class MockedHttpSession:
        def get(self, url, timeout, headers):
            raise requests.exceptions.Timeout

    def setup():
        return Requester(auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA",
                         retries=2,
                         timeout=4,
                         cache_ttl=172800, session=MockedHttpSession())
    requester = setup()

    resp = requester.get(url="https://mock-api-challenge.dev.iclinic.com.br/physicians/1/")
    assert type(resp) == dict
    assert 'error' in resp
    assert 'message' in resp['error']
    assert 'code' in resp['error']
    assert resp['error']['message'] == Errors.REQUEST_TIMEOUT.message
    assert resp['error']['code'] == Errors.REQUEST_TIMEOUT.code


def test_requester_get_http_error():
    class MockedHttpSession:
        def get(self, url, timeout, headers):
            raise requests.exceptions.HTTPError

    def setup():
        return Requester(auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA",
                         retries=2,
                         timeout=4,
                         cache_ttl=172800, session=MockedHttpSession())
    requester = setup()

    resp = requester.get(url="https://mock-api-challenge.dev.iclinic.com.br/physicians/1/")
    assert type(resp) == dict
    assert 'error' in resp
    assert 'message' in resp['error']
    assert 'code' in resp['error']
    assert resp['error']['message'] == Errors.HTTP_ERROR.message
    assert resp['error']['code'] == Errors.HTTP_ERROR.code


def test_requester_invalid_url():
    def setup():
        return Requester(auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA",
                         retries=2,
                         timeout=4,
                         cache_ttl=172800)
    requester = setup()

    resp = requester.get(url="https://")
    assert type(resp) == dict
    assert 'error' in resp
    assert 'message' in resp['error']
    assert 'code' in resp['error']
    assert resp['error']['message'] == Errors.INVALID_URL.message
    assert resp['error']['code'] == Errors.INVALID_URL.code


def test_requester_get_status_code():
    class MockedHttpSession:
        def get(self, url, timeout, headers):
            class Response:
                status_code = 404

            return Response()

    def setup():
        return Requester(auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA",
                         retries=2,
                         timeout=4,
                         cache_ttl=172800, session=MockedHttpSession())
    requester = setup()

    resp = requester.get(url="https://mock-api-challenge.dev.iclinic.com.br/physicians/1/")
    assert type(resp) == dict
    assert 'error' in resp
    assert 'message' in resp['error']
    assert 'code' in resp['error']
    assert resp['error']['message'] == 'http status'
    assert resp['error']['code'] == 404


def test_requester_post_timeout():
    class MockedHttpSession:
        def post(self, url, timeout, headers, json):
            raise requests.exceptions.Timeout

    def setup():
        return Requester(auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA",
                         retries=2,
                         timeout=4,
                         cache_ttl=172800, session=MockedHttpSession())
    requester = setup()

    resp = requester.post(url="https://mock-api-challenge.dev.iclinic.com.br/physicians/1/", content={})
    assert type(resp) == dict
    assert 'error' in resp
    assert 'message' in resp['error']
    assert 'code' in resp['error']
    assert resp['error']['message'] == Errors.REQUEST_TIMEOUT.message
    assert resp['error']['code'] == Errors.REQUEST_TIMEOUT.code


def test_requester_post_http_error():
    class MockedHttpSession:
        def post(self, url, timeout, headers, json):
            raise requests.exceptions.HTTPError

    def setup():
        return Requester(auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA",
                         retries=2,
                         timeout=4,
                         cache_ttl=172800, session=MockedHttpSession())
    requester = setup()

    resp = requester.post(url="https://mock-api-challenge.dev.iclinic.com.br/physicians/1/", content={})
    assert type(resp) == dict
    assert 'error' in resp
    assert 'message' in resp['error']
    assert 'code' in resp['error']
    assert resp['error']['message'] == Errors.HTTP_ERROR.message
    assert resp['error']['code'] == Errors.HTTP_ERROR.code


def test_requester_post_status_code():
    class MockedHttpSession:
        def post(self, url, timeout, headers, json):
            class Response:
                status_code = 404

            return Response()

    def setup():
        return Requester(auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA",
                         retries=2,
                         timeout=4,
                         cache_ttl=172800, session=MockedHttpSession())
    requester = setup()

    resp = requester.post(url="https://mock-api-challenge.dev.iclinic.com.br/physicians/1/", content={})
    assert type(resp) == dict
    assert 'error' in resp
    assert 'message' in resp['error']
    assert 'code' in resp['error']
    assert resp['error']['message'] == 'http status'
    assert resp['error']['code'] == 404


def test_requester_post_success():
    class MockedHttpSession:
        def post(self, url, timeout, headers, json):
            class Response:
                status_code = 201

                def json(self):
                    return {
                            "id": "58e556b8-0727-4041-b78c-102655b880f7",
                            "clinic_id": 1,
                            "clinic_name": "Clinica A",
                            "physician_id": 1,
                            "physician_name": "José",
                            "physician_crm": "SP293893",
                            "patient_id": 1,
                            "patient_name": "Rodrigo",
                            "patient_email": "rodrigo@gmail.com",
                            "patient_phone": "(16)998765625",
                            "prescription_id": 1
                        }

            return Response()

    def setup():
        return Requester(auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA",
                         retries=2,
                         timeout=4,
                         cache_ttl=172800, session=MockedHttpSession())
    requester = setup()

    resp = requester.post(url="https://mock-api-challenge.dev.iclinic.com.br/physicians/1/", content={})
    assert type(resp) == dict
    assert 'id' in resp
    assert 'clinic_id' in resp
    assert 'clinic_name' in resp
    assert 'physician_id' in resp
    assert 'physician_name' in resp
    assert 'physician_crm' in resp
    assert 'patient_id' in resp
    assert 'patient_name' in resp
    assert 'patient_email' in resp
    assert 'patient_phone' in resp
    assert 'prescription_id' in resp