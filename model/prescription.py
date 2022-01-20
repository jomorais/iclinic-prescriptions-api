from dataclasses import dataclass


@dataclass
class Prescription:
    id: str = ''
    clinic_id: int = 0
    physician_id: int = 0
    patient_id: int = 0
    text: str = ''
    metric_id: str = ''

    def build_json(self):
        return {"data": {"id": self.id,
                         "clinic_id": self.clinic_id,
                         "physician_id": self.physician_id,
                         "text": self.text,
                         "metric_id": self.metric_id}}
