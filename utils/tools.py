
def mandatory_keys_checker(mandatory_keys: list, dict_object: dict):
    if type(mandatory_keys) != list:
        raise Exception("keys must be a list: keys=['key_1', 'key_2', ..., 'key_n']")
    if type(dict_object) != dict:
        raise Exception("keys must be a dict: dict={'key_1': 'value_1', 'key_2': 'value_2', ..., 'key_n': 'value_n'}}")
    if all(k in dict_object for k in mandatory_keys):
        return True
    return False



