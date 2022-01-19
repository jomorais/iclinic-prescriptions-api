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


@dataclass
class Error:
    message: str = ''
    code: int = 0

    def build_json(self):
        return {"error": {"message": self.message, "code": self.code}}


@dataclass
class Errors:
    MALFORMED_REQUEST: Error = Error(message="malformed request",
                                     code=MALFORMED_REQUEST)
    PHYSICIAN_NOT_FOUND: Error = Error(message="physician not found",
                                       code=PHYSICIAN_NOT_FOUND)
    PATIENT_NOT_FOUND: Error = Error(message="patient not found",
                                     code=PATIENT_NOT_FOUND)
    METRICS_SERVICE_NOT_AVAILABLE: Error = Error(message="metrics service not available",
                                                 code=METRICS_SERVICE_NOT_AVAILABLE)
    PHYSICIANS_SERVICE_NOT_AVAILABLE: Error = Error(message="physicians service not available",
                                                    code=PHYSICIANS_SERVICE_NOT_AVAILABLE)
    PATIENTS_SERVICE_NOT_AVAILABLE: Error = Error(message="patients service not available",
                                                  code=PATIENTS_SERVICE_NOT_AVAILABLE)
    CLINIC_NOT_FOUND: Error = Error(message="clinic not found",
                                    code=CLINIC_NOT_FOUND)
    CLINICS_SERVICE_NOT_AVAILABLE: Error = Error(message="clinics service not available",
                                                 code=CLINICS_SERVICE_NOT_AVAILABLE)
    REQUEST_TIMEOUT: Error = Error(message="request timeout",
                                   code=REQUEST_TIMEOUT)
    HTTP_ERROR: Error = Error(message="http error",
                              code=HTTP_ERROR)
