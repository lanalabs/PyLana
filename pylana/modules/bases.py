import functools
import warnings

import requests

from pylana.modules.structures import User
from pylana.modules.user_management import get_user_information
from pylana.utils import _create_headers
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


# TODO: consider certificate passing for TLS
class API:

    def __init__(self, scheme: str, host: str, token: str, port: int = None):

        self.url = f'{scheme}://{host}' + (f':{port}' if port else '')
        user_info = get_user_information(scheme, host, token, port)
        self.user = User(user_id=user_info.get('id'),
                         organization_id=user_info.get('organizationId'),
                         api_key=user_info.get('apiKey'),
                         role=user_info.get('role'))
        self.headers = _create_headers(token)

        # legacy
        self.user_info = user_info

    def _request(self, method, route, additional_headers=None, **kwargs):
        headers = {**self.headers, **(additional_headers or dict())}
        return requests.request(method, self.url + route, headers=headers, **kwargs)

    @handle_response
    def get(self, route, additional_headers=None, **kwargs):
        return self._request('GET', route, additional_headers, **kwargs)

    @handle_response
    def post(self, route, additional_headers=None, **kwargs):
        return self._request('POST', route, additional_headers, **kwargs)

    @handle_response
    def patch(self, route, additional_headers=None, **kwargs):
        return self._request('PATCH', route, additional_headers, **kwargs)

    @handle_response
    def delete(self, route, additional_headers=None, **kwargs):
        return self._request('DELETE', route, additional_headers, **kwargs)
