from dataclasses import dataclass


@dataclass
class Physician:
    id: int = 0
    name: str = ""
    crm: str = ""
    schema = {
        "id": "physician",
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
            "crm": {"type": "string"}
        },
        "required": ["id", "name", "crm"]
    }

    def build_json(self):
        return {"id": self.id,
                "name": self.name,
                "crm": self.crm}
