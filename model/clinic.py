from dataclasses import dataclass


@dataclass
class Clinic:
    id: int = 0
    name: str = ""

    def build_json(self):
        return {"id": self.id, "name": self.name}
