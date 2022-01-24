from services.settings import schema, dependent_services_settings
from utils.tools import validate_json


def test_settings():
    assert validate_json(json_object=dependent_services_settings, schema=schema)
