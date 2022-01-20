from dataclasses import dataclass

"""
01	malformed request
02	physician not found
03	patient not found
04	metrics service not available
05	physicians service not available
06	patients service not available
07  clinic not found
08  clinics service not available
09  request timeout
10  http error
"""


class ErrorCode:
    MALFORMED_REQUEST = 1
    PHYSICIAN_NOT_FOUND = 2
    PATIENT_NOT_FOUND = 3
    METRICS_SERVICE_NOT_AVAILABLE = 4
    PHYSICIANS_SERVICE_NOT_AVAILABLE = 5
    PATIENTS_SERVICE_NOT_AVAILABLE = 6
    CLINIC_NOT_FOUND = 7
    CLINICS_SERVICE_NOT_AVAILABLE = 8
    REQUEST_TIMEOUT = 9
    HTTP_ERROR = 10
    INVALID_URL = 11
    HTTP_STATUS = 12
    DATABASE_ERROR = 13
    PRESCRIPTION_NOT_FOUND = 14


@dataclass
class Error:
    message: str = ''
    code: int = 0

    def build_json(self, message='', code=0):
        if message != '':
            self.message = message
        if code != 0:
            self.code = code
        return {"error": {"message": self.message, "code": self.code}}


@dataclass
class Errors:
    MALFORMED_REQUEST: Error = Error(message="malformed request",
                                     code=ErrorCode.MALFORMED_REQUEST)
    PHYSICIAN_NOT_FOUND: Error = Error(message="physician not found",
                                       code=ErrorCode.PHYSICIAN_NOT_FOUND)
    PATIENT_NOT_FOUND: Error = Error(message="patient not found",
                                     code=ErrorCode.PATIENT_NOT_FOUND)
    METRICS_SERVICE_NOT_AVAILABLE: Error = Error(message="metrics service not available",
                                                 code=ErrorCode.METRICS_SERVICE_NOT_AVAILABLE)
    PHYSICIANS_SERVICE_NOT_AVAILABLE: Error = Error(message="physicians service not available",
                                                    code=ErrorCode.PHYSICIANS_SERVICE_NOT_AVAILABLE)
    PATIENTS_SERVICE_NOT_AVAILABLE: Error = Error(message="patients service not available",
                                                  code=ErrorCode.PATIENTS_SERVICE_NOT_AVAILABLE)
    CLINIC_NOT_FOUND: Error = Error(message="clinic not found",
                                    code=ErrorCode.CLINIC_NOT_FOUND)
    CLINICS_SERVICE_NOT_AVAILABLE: Error = Error(message="clinics service not available",
                                                 code=ErrorCode.CLINICS_SERVICE_NOT_AVAILABLE)
    REQUEST_TIMEOUT: Error = Error(message="request timeout",
                                   code=ErrorCode.REQUEST_TIMEOUT)
    HTTP_ERROR: Error = Error(message="http error",
                              code=ErrorCode.HTTP_ERROR)
    INVALID_URL: Error = Error(message="invalid url",
                               code=ErrorCode.INVALID_URL)
    HTTP_STATUS: Error = Error(message="http status")
    DATABASE_ERROR: Error = Error(message="database error", code=ErrorCode.DATABASE_ERROR)
    PRESCRIPTION_NOT_FOUND: Error = Error(message="prescription not found", code=ErrorCode.PRESCRIPTION_NOT_FOUND)
