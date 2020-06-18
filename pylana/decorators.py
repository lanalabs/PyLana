"""
decorators for handling api request responses
"""

import functools
import json
from typing import List

import requests


def expect_json(method):
    @functools.wraps(method)
    def parse_json(*args, **kwargs) -> List[dict]:
        resp = method(*args, **kwargs)
        try:
            jsn = resp.json()
        except json.decoder.JSONDecodeError as e:
            mime_type = resp.headers.get('Content-Type')
            raise Exception(f'Expected mime-type application/json got {mime_type}')
        return jsn
    return parse_json


# TODO: introduce proper logging
def handle_response(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs) -> requests.Response:
        resp = method(*args, **kwargs)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
        return resp
    return wrapper
