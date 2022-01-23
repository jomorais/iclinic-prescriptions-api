from dataclasses import dataclass


@dataclass
class HttpResponse:
    json: dict
    code: int = 0
