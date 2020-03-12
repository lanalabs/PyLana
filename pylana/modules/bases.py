import abc
import functools
import warnings

import requests

from pylana.utils import handle_response


def handle_http_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            pass
            warnings.warn(str(e), Warning)

        return resp
    return wrapper


class _API(abc.ABC):

    url: str
    headers: dict

    @handle_response
    def get(self, route, additional_headers=None, **kwargs):
        headers = {**self.headers, **(additional_headers or dict())}
        resp = requests.get(self.url + route, headers=headers, **kwargs)
        return resp

    @handle_response
    def post(self, route, additional_headers=None, **kwargs):
        headers = {**self.headers, **(additional_headers or dict())}
        resp = requests.post(self.url + route, headers=headers, **kwargs)
        return resp

    @handle_response
    def patch(self, route, additional_headers=None, **kwargs):
        headers = {**self.headers, **(additional_headers or dict())}
        resp = requests.patch(self.url + route, headers=headers, **kwargs)
        return resp