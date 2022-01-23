from dataclasses import dataclass


class ErrorCode:
    CODE_MALFORMED_REQUEST = 1
    CODE_PHYSICIAN_NOT_FOUND = 2
    CODE_PATIENT_NOT_FOUND = 3
    CODE_METRICS_SERVICE_NOT_AVAILABLE = 4
    CODE_PHYSICIANS_SERVICE_NOT_AVAILABLE = 5
    CODE_PATIENTS_SERVICE_NOT_AVAILABLE = 6
    CODE_CLINIC_NOT_FOUND = 7
    CODE_CLINICS_SERVICE_NOT_AVAILABLE = 8
    CODE_REQUEST_TIMEOUT = 9
    CODE_HTTP_ERROR = 10
    CODE_INVALID_URL = 11
    CODE_HTTP_STATUS = 12
    CODE_DATABASE_ERROR = 13
    CODE_INVALID_CLINICS_SERVICE_RESPONSE = 14
    CODE_INVALID_PATIENTS_SERVICE_RESPONSE = 15
    CODE_INVALID_PHYSICIANS_SERVICE_RESPONSE = 16
    CODE_INVALID_METRICS_SERVICE_RESPONSE = 17


@dataclass
class Error:
    message: str = ''
    code: int = 0
    http_code: int = 400

    def build_json(self, message='', code=0):
        if message != '':
            self.message = message
        if code != 0:
            self.code = code
        return {"error": {"message": self.message, "code": self.code}}


@dataclass
class Errors:
    MALFORMED_REQUEST: Error = Error(message="malformed request",
                                     code=ErrorCode.CODE_MALFORMED_REQUEST,
                                     http_code=400)
    REQUEST_TIMEOUT: Error = Error(message="request timeout",
                                   code=ErrorCode.CODE_REQUEST_TIMEOUT,
                                   http_code=408)
    HTTP_ERROR: Error = Error(message="http error",
                              code=ErrorCode.CODE_HTTP_ERROR,
                              http_code=500)
    INVALID_URL: Error = Error(message="invalid url",
                               code=ErrorCode.CODE_INVALID_URL,
                               http_code=400)
    DATABASE_ERROR: Error = Error(message="database error",
                                  code=ErrorCode.CODE_DATABASE_ERROR,
                                  http_code=500)
    HTTP_STATUS: Error = Error(message="http status")


@dataclass
class iClinicErrors:
    PHYSICIAN_NOT_FOUND: Error = Error(message="physician not found",
                                       code=ErrorCode.CODE_PHYSICIAN_NOT_FOUND,
                                       http_code=404)
    PATIENT_NOT_FOUND: Error = Error(message="patient not found",
                                     code=ErrorCode.CODE_PATIENT_NOT_FOUND,
                                     http_code=404)
    METRICS_SERVICE_NOT_AVAILABLE: Error = Error(message="metrics service not available",
                                                 code=ErrorCode.CODE_METRICS_SERVICE_NOT_AVAILABLE,
                                                 http_code=503)
    PHYSICIANS_SERVICE_NOT_AVAILABLE: Error = Error(message="physicians service not available",
                                                    code=ErrorCode.CODE_PHYSICIANS_SERVICE_NOT_AVAILABLE,
                                                    http_code=503)
    PATIENTS_SERVICE_NOT_AVAILABLE: Error = Error(message="patients service not available",
                                                  code=ErrorCode.CODE_PATIENTS_SERVICE_NOT_AVAILABLE,
                                                  http_code=503)
    CLINIC_NOT_FOUND: Error = Error(message="clinic not found",
                                    code=ErrorCode.CODE_CLINIC_NOT_FOUND,
                                    http_code=404)
    CLINICS_SERVICE_NOT_AVAILABLE: Error = Error(message="clinics service not available",
                                                 code=ErrorCode.CODE_CLINICS_SERVICE_NOT_AVAILABLE,
                                                 http_code=503)
    INVALID_CLINICS_SERVICE_RESPONSE: Error = Error(message="invalid clinics service response",
                                                    code=ErrorCode.CODE_INVALID_CLINICS_SERVICE_RESPONSE,
                                                    http_code=500)
    INVALID_PATIENTS_SERVICE_RESPONSE: Error = Error(message="invalid patients service response",
                                                     code=ErrorCode.CODE_INVALID_PATIENTS_SERVICE_RESPONSE,
                                                     http_code=500)
    INVALID_PHYSICIANS_SERVICE_RESPONSE: Error = Error(message="invalid physicians service response",
                                                       code=ErrorCode.CODE_INVALID_PHYSICIANS_SERVICE_RESPONSE,
                                                       http_code=500)
    INVALID_METRICS_SERVICE_RESPONSE: Error = Error(message="invalid metrics service response",
                                                    code=ErrorCode.CODE_INVALID_METRICS_SERVICE_RESPONSE,
                                                    http_code=500)
