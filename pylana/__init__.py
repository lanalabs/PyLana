"""
Methods for creating the python API for LANA Process Mining.
"""

import functools
import warnings

from pylana.v1 import LanaAPI
from pylana.v2 import LanaAPI2

name = "pylana"


def create_api(scheme, host, token, port=None, compatibility=False, url=None, verify=False):
    """
    create a Lana API instance

    It is still possible to create an api conform with old versions of
    PyLana, if absolutely necessary. It will be phased out over time,
    as most of its functinoality moves into the new version,

    Args:
        scheme:
            A string denoting the scheme of the connection to Lana, usually
            http or https.
        host:
            A string denoting the host of the Lana API.
        token:
            A string representing the user token used for user authentication.
        port:
            (optional) An integer or string denoting the port for the lana
            api. If not set, default ports for the scheme are be used.
        verify:
            (optional) If set to False, disables TLS certification
            verification.
        compatibility:
            (optional) A boolean indicating whether the legacy PyLana should
            be created.
        url:
            (optional) If compatibility is True, you can pass the base url
            as "<scheme>://<host>:<port>/".
    """

    if compatibility:
        warnings.warn(
            DeprecationWarning(
                'Support for the old PyLana api will deprecate soon.'
            )
        )
        url = url if url else f'{scheme}://{host}:{port}/'
        return LanaAPI(url, token=token)

    api = LanaAPI2(scheme, host, token, port)
    api._request = functools.partial(api._request, verify=verify)

    return api
