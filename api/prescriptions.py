from services.clinicsservice import ClinicsService
from services.patientsservice import PatientsService
from services.physiciansservice import PhysiciansService
from services.metricsservice import MetricsService
from model.prescription import Prescription


class Prescritions:
    def __init__(self, database):
        self.database = database
        self.clinics_service = ClinicsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                                              path="/clinics/", retries=3, timeout=5, cache_ttl=259200,
                                              auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ")
        self.patients_service = PatientsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                                                path="/patients/", retries=2, timeout=3, cache_ttl=43200,
                                                auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGF0aWVudHMifQ.Pr6Z58GzNRtjX8Y09hEBzl7dluxsGiaxGlfzdaphzVU")
        self.physicians_service = PhysiciansService(host="https://mock-api-challenge.dev.iclinic.com.br",
                                                    path="/physicians/", retries=2, timeout=4, cache_ttl=172800,
                                                    auth_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA")
        self.metrics_service = MetricsService(host="https://mock-api-challenge.dev.iclinic.com.br",
                                              path="/metrics/", retries=5, timeout=6, cache_ttl=0,
                                              auth_token="Bearer SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")