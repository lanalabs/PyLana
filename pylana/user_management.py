"""
user management functions
"""

import requests

from .structures import User
from .utils import _create_authorization_header
from .decorators import handle_response, expect_json


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
