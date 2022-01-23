from dataclasses import dataclass


@dataclass
class Patient:
    id: int = 0
    name: str = ""
    email: str = ""
    phone: str = ""
    schema = {
        "id": "patient",
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
            "email": {"type": "string"},
            "phone": {"type": "string"}
        },
        "required": ["id", "name", "email", "phone"]
    }

    def build_json(self):
        return {"id": self.id, "name": self.name, "email": self.email, "phone": self.phone}
