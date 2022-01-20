from dataclasses import dataclass


@dataclass
class Patient:
    id: int = 0
    name: str = ""
    email: str = ""
    phone: str = ""

    def build_json(self):
        return {"id": self.id, "name": self.name, "email": self.email, "phone": self.phone}
