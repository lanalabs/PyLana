import functools
from typing import List

import json


def _create_headers(token: str):
    return {"Authorization": f"API-Key {token}"}


def expect_json(func):
    @functools.wraps(func)
    def parse_json(*args, **kwargs) -> List[dict]:
        resp = func(*args, **kwargs)
        try:
            jsn = resp.json()
        except json.decoder.JSONDecodeError as e:
            mime_type = resp.headers.get('Content-Type')
            raise Exception(f'Expected application/json got {mime_type}')
        return jsn
    return parse_json

