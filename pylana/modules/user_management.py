import requests

from pylana.utils import _create_headers
from pylana.utils import expect_json


@expect_json
def get_user_information(scheme: str, host: str, token: str, port=None) -> dict:

    base_url = f'{scheme}://{host}' + (f':{port}' if port else '')
    headers = _create_headers(token)

    resp = requests.get(base_url + '/api/users/by-token', headers=headers)
    resp.raise_for_status()

    return resp
