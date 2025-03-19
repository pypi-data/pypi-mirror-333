import json
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    """json.dumps(data, cls=DateTimeEncoder)"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def decode_datetime(dct):
    """json.loads(f.read(), object_hook=decode_datetime)"""
    for key, value in dct.items():
        try:
            # Attempt to parse the value as a datetime string
            dct[key] = datetime.fromisoformat(value)
        except (ValueError, TypeError):
            # If it's not a valid datetime string, leave it as is
            pass
    return dct
