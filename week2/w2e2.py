import json
import functools

def to_json(func):
    @functools.wraps(func)
    def wrappped(*args, **kwargs):
        answer = func(*args, **kwargs)
        return json.dumps(answer)
    return wrappped