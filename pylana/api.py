"""
generic api requests including authorization
"""

from typing import Optional

import requests

from pylana.decorators import handle_response, expect_json
from pylana.structures import User


def _create_authorization_header(token: str) -> dict:
    return {"Authorization": f"API-Key {token}"}


@expect_json
@handle_response
def get_user_information(scheme: str, host: str, token: str,
                         port=None) -> dict:
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


# TODO consider certificate passing for TLS
# TODO consider letting kwargs replace authentication header
class API:
    """An api for a specific user at a Lana deployment.

    All required information to make authenticated requests to the api are
    passed during construction and stored. Named request methods are
    provided as wrappers around requests library methods, that add required
    header fields. Additional headers to the requests library methods can be
    passed as keyword arguments.

    Attributes:
        url (str):
            The base url of the api (scheme, host and port).
        user (User):
            A User dataclass encapsulating the user of the api information.
        headers (dict):
            The authorization header used for every request by default.
    """

    # TODO document
    def __init__(self, scheme: str, host: str, token: str,
                 port: Optional[int] = None, application_root: Optional[str] = None):
        self.url = (f'{scheme}://{host}'
                    + (f':{port}' if port else '')
                    + (f':{application_root}'
                       if application_root else '').replace('//', '/')
                    ).strip('/')
        user_info = get_user_information(scheme, host, token, port)
        self.user = User(user_id=user_info.get('id'),
                         organization_id=user_info.get('organizationId'),
                         api_key=user_info.get('apiKey'),
                         role=user_info.get('role'))
        self.headers = _create_authorization_header(token)

    def _request(self, method, route, headers=None, additional_headers=None,
                 **kwargs):
        headers = {**self.headers, **(additional_headers or dict()),
                   **(headers or dict())}
        return requests.request(method, self.url + route, headers=headers,
                                **kwargs)

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
