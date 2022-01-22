from dataclasses import dataclass


@dataclass
class Physician:
    id: int = 0
    name: str = ""
    crm: str = ""

    def build_json(self):
        return {"id": self.id,
                "name": self.name,
                "crm": self.crm}