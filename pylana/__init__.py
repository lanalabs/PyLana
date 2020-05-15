"""
Python API for LANA Process Mining
"""

import functools
import warnings

from pylana.v1 import LanaAPI
from pylana.v2 import LanaAPI2

name = "pylana"


def create_api(scheme, host, token, port=None, compatibility=False, url=None, verify=False):
    """
    create a Lana API instance

    It is still possible to create an api conform with old versions of PyLana, if absolutely necessary.
    It will be phased out over time, as most oif its functionalities move into the new version,

    Args:
        scheme: a string denoting the scheme of the connection to lan a, usually http or https
        host: a string denoting the host of the lana api
        token: a string representing the user token used for authenticating at the api
        port: (optional) the port for the lana api, if not set default ports for the scheme will be used
        verify: (optional) if set to false, disables tls certification verification
        compatibility: (optional) a boolean indicating whether an older python interfac e for lana should be used
        url: (optional) if compatibility is True, you can pass the base url as "<scheme>://<host>:<port>/"
    """

    if compatibility:
        warnings.warn(DeprecationWarning('Support for the old PyLana api will deprecate soon.'))
        url = url if url else f'{scheme}://{host}:{port}/'
        return LanaAPI(url, token=token)

    api = LanaAPI2(scheme, host, token, port)
    api._request = functools.partial(api._request, verify=verify)

    return api
