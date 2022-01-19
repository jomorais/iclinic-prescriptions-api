import pytest
from utils.utils import mandatory_keys_checker


def test_key_checker():
    my_dict = {"key_a": "aaa", "key_b": "bbb", "key_c": 0, "key_d": 0.1, "key_e": {}}

    assert mandatory_keys_checker(['key_a', 'key_b', 'key_c', 'key_d', 'key_e'], dict_object=my_dict) is True

    assert mandatory_keys_checker(['key_b', 'key_c', 'key_d', 'key_e'], dict_object=my_dict) is True

    assert mandatory_keys_checker(['key_a'], dict_object=my_dict) is True

    with pytest.raises(Exception):
        mandatory_keys_checker('key_a', dict_object=my_dict)

    with pytest.raises(Exception):
        mandatory_keys_checker(['key_a'], dict_object='')

    assert mandatory_keys_checker(['key_a', 'key_b', 'key_c', 'key_d', 'key_e', 'key_f'], dict_object=my_dict) is False

    assert mandatory_keys_checker(['key_b', 'key_c', 'key_d', 'key_e', 'key_f'], dict_object=my_dict) is False