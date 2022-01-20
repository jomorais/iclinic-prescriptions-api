from dataclasses import dataclass


@dataclass
class Physician:
    id: int = 0
    name: str = ""
    crm: str = ""