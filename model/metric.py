from dataclasses import dataclass
from model.clinic import Clinic
from model.patient import Patient
from model.physician import Physician


@dataclass
class Metric:
    id: str = ''
    clinic_id: int = 0
    clinic_name: str = ''
    physician_id: int = 0
    physician_name: str = ''
    physician_crm: str = ''
    patient_id: int = 0
    patient_name: str = ''
    patient_email: str = ''
    patient_phone: str = ''
    prescription_id: int = 0

    def set_clinic(self, clinic: Clinic):
        self.clinic_id = clinic.id
        self.clinic_name = clinic.name

    def set_physician(self, physician: Physician):
        self.physician_id = physician.id
        self.physician_name = physician.name
        self.physician_crm = physician.crm

    def set_patient(self, patient: Patient):
        self.patient_id = patient.id
        self.patient_name = patient.name
        self.patient_phone = patient.phone
        self.patient_email = patient.email

    def build_json(self):
        if self.clinic_id > 0:
            return {"id": self.id,
                    "clinic_id": self.clinic_id,
                    "clinic_name": self.clinic_name,
                    "physician_id": self.physician_id,
                    "physician_name": self.physician_name,
                    "physician_crm": self.physician_crm,
                    "patient_id": self.patient_id,
                    "patient_name": self.patient_name,
                    "patient_email": self.patient_email,
                    "patient_phone": self.patient_phone,
                    "prescription_id": self.prescription_id,
                    }
        return {"id": self.id,
                "physician_id": self.physician_id,
                "physician_name": self.physician_name,
                "physician_crm": self.physician_crm,
                "patient_id": self.patient_id,
                "patient_name": self.patient_name,
                "patient_email": self.patient_email,
                "patient_phone": self.patient_phone,
                "prescription_id": self.prescription_id,
                }