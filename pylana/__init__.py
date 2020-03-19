'''
pylana
=================================
Python API for LANA Process Mining
'''

import functools

from pylana.pylana import LanaAPI
from pylana.pylana_v2 import LanaAPI2


import pylana.modules


name = "pylana"


def create_api(scheme, host, token, port=None,
               verify=False, compatibility=False, url=None, api_key=None):
    """
    create a Lana API instance
    """

    if compatibility:
        url = url if url else f'{scheme}://{host}:{port}/'
        return LanaAPI(url, token, api_key)

    api = LanaAPI2(scheme, host, token, port)
    api._request = functools.partial(api._request, verify=verify)

    return api
