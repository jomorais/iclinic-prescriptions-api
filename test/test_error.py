from utils.error import Errors, Error


def test_error():
    error = Error()
    assert error.message == ""
    assert error.code == 0
    assert error.build_json() == {"error": {"message": "", "code": 0}}


def test_errors():
    assert Errors.MALFORMED_REQUEST.code == 1
    assert Errors.MALFORMED_REQUEST.message == "malformed request"
    assert Errors.MALFORMED_REQUEST.build_json() == {"error": {"message": "malformed request", "code": 1}}
    assert Errors.MALFORMED_REQUEST.build_json(message="ABC") == {"error": {"message": "ABC", "code": 1}}
    assert Errors.MALFORMED_REQUEST.build_json(code=123) == {"error": {"message": "ABC", "code": 123}}
