from jsonschema import validate
from jsonschema.exceptions import ValidationError


def validate_json(json_object: dict, schema: dict):
    try:
        validate(instance=json_object, schema=schema)
        return True
    except ValidationError:
        return False



