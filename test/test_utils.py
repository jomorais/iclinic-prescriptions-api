import pytest
from utils.tools import validate_json
from model.prescription import Prescription


def test_validate_json():
    def setup():
        prescription_json = {
          "clinic": {
                "id": 1
          },
          "physician": {
            "id": 1
          },
          "patient": {
            "id": 2
          },
          "text": "Dipirona 1x ao diaasdasd"
        }
        return prescription_json
    prescription_json = setup()
    assert validate_json(json_object=prescription_json, schema=Prescription.schema)


def test_validate_failed():
    def setup():
        prescription_json = {
          "clinic": {
                "ids": 1
          },
          "physician": {
            "id": 1
          },
          "patient": {
            "id": 2
          },
          "text": "Dipirona 1x ao diaasdasd"
        }
        return prescription_json
    prescription_json = setup()
    assert validate_json(json_object=prescription_json, schema=Prescription.schema) is False
