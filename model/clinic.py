from dataclasses import dataclass


@dataclass
class Clinic:
    id: int = 0
    name: str = ""
    schema = {
        "id": "clinic",
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"}
        },
        "required": ["id", "name"]
    }

    def build_json(self):
        return {"id": self.id, "name": self.name}
