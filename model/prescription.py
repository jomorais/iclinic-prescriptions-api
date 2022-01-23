from dataclasses import dataclass


@dataclass
class Prescription:
    id: int = 0
    clinic_id: int = 0
    physician_id: int = 0
    patient_id: int = 0
    text: str = ''
    metric_id: str = ''
    schema = {
      "id": "prescription",
      "type": "object",
      "properties": {
        "clinic": {
          "type": "object",
          "properties": {
            "id": {"type": "number"}
          },
          "required": ["id"]
        },
        "physician": {
          "type": "object",
          "properties": {
            "id": {"type": "number"}
          },
          "required": ["id"]
        },
        "patient": {
          "type": "object",
          "properties": {
            "id": {"type": "number"}
          },
          "required": ["id"]
        },
        "text": {"type": "string"},
      },
      "required": ["clinic", "physician", "patient", "text"]
    }

    def build_json(self):
        return {"data": {"id": self.id,
                         "clinic": {"id": self.clinic_id},
                         "physician": {"id": self.physician_id},
                         "patient": {"id": self.patient_id},
                         "text": self.text,
                         "metric": {"id": self.metric_id}}}