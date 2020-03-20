import functools
import json
import re
from typing import List

import requests


def _create_headers(token: str):
    return {"Authorization": f"API-Key {token}"}


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
    def wrapper(*args, **kwargs):
        resp = method(*args, **kwargs)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
        return resp
    return wrapper


def extract_ids(method):
    @functools.wraps(method)
    def wrapper(self, contains, **kwargs):
        resources = method(self, contains, **kwargs)
        rc = re.compile(contains)
        return [log['id'] for log in resources if rc.search(log['name'])]
    return wrapper


def extract_id(method):
    @functools.wraps(method)
    def wrapper(self, contains, **kwargs):
        ids = method(self, contains, **kwargs)
        try:
            [id_] = ids
        except ValueError as e:
            raise Exception(f'Found {len(ids)} resources with the pattern {contains}')

        return id_
    return wrapper
