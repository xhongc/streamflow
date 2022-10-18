import json


def try_json(val):
    if isinstance(val, str):
        try:
            val = json.loads(val)
            return val
        except Exception:
            raise Exception("json序列化失败")
    else:
        return val
