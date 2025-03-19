import json


def sort_dict_by_keys(data: dict):
    return dict(sorted(data.items(), key=lambda x: x[0]))


def sort_nested_dict_by_values(data: dict):
    return json.loads(json.dumps(data, sort_keys=True))


def sort_dict_by_values(data: dict):
    return dict(sorted(data.items(), key=lambda x: x[1]))
