"""
generic api requests including authorization
"""

import requests

from pylana.decorators import handle_response, expect_json
from pylana.structures import User


def _create_authorization_header(token: str) -> dict:
    return {"Authorization": f"API-Key {token}"}


@expect_json
@handle_response
def get_user_information(scheme: str, host: str, token: str, port=None) -> dict:

    base_url = f'{scheme}://{host}' + (f':{port}' if port else '')
    headers = _create_authorization_header(token)
    r = requests.get(base_url + '/api/users/by-token', headers=headers)
    r.raise_for_status()
    return r


def get_user(scheme: str, host: str, token: str, port=None) -> User:
    user_info = get_user_information(scheme, host, token, port)
    return User(user_id=user_info.get('id'),
                organization_id=user_info.get('organizationId'),
                api_key=user_info.get('apiKey'),
                role=user_info.get('role'))


# TODO: consider certificate passing for TLS
class API:
    """
    an api for a specific user at a Lana deployment

    Attributes:
        url (str): the base url of the api (scheme, host and port)
        user (User): a User dataclass encapsulating the user of the api information
        headers (dict): the authorization header
    """

    def __init__(self, scheme: str, host: str, token: str, port: int = None):

        self.url = f'{scheme}://{host}' + (f':{port}' if port else '')
        user_info = get_user_information(scheme, host, token, port)
        self.user = User(user_id=user_info.get('id'),
                         organization_id=user_info.get('organizationId'),
                         api_key=user_info.get('apiKey'),
                         role=user_info.get('role'))
        self.headers = _create_authorization_header(token)

    def _request(self, method, route, headers=None, additional_headers=None, **kwargs):
        headers = {**self.headers, **(additional_headers or dict()), **(headers or dict())}
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
