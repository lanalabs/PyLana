"""
Methods for creating the python API for LANA Process Mining.
"""

import functools
import warnings

from pylana.v1 import LanaAPI
from pylana.v2 import LanaAPI2


def create_api(scheme, host, token, port=None, compatibility=False,
               url=None, verify=False, application_root=None, **kwargs):
    """Create a configured Lana API.

    The returned api stores the url for a LANA Process Mining
    api as well as your authentication. After creation you can us it to
    manage the LANA process mining resources. Among other things you can
    upload data from python pandas data frames directly or connect logs
    and shiny dashboard resources referencing them by their names.

        api = create_api('https', 'cloud-backend.lanalabs.com', '<a token>')
        upload_response = api.upload_event_log_df(
                                'new-event-log', df_event_log,
                                time_format='YYYY-mm-dd,
                                df_case=df_case_attributes)
        shiny_dashboard = api.create_shiny_dashboard('new-shiny-dashboard')
        connection_response = api.connect_shiny_dashboard(
                                    upload_response.json()['id'],
                                    shiny_dashboard['id'])

    It also provides basic methods to make HTTP verb requests
    directly to the lana endpoints. For example

        response_list = api.get('/api/v2/dashboards')

    Will return a response with a list of dashboard metadata.

    We try to provide the old api of pre-0.1.0 PyLana, but can't guarantee
    that it stays around forever. In case you absolutely require the old
    interface, you can pass compatibility as True, which creates an old Lana
    API instance.

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
            (optional) Either a boolean, in which case it controls whether we
            verify the server’s TLS certificate, or a string, in which case it
            must be a path to a CA bundle to use. Defaults to False.
        application_root:
            (optional) A string denoting the application root. Only required
            if your lana api is placed outside the URL root, e.g. "/lana-api"
            instead of "/". Has to start with a slash.
        compatibility:
            (optional) A boolean indicating whether the legacy PyLana should
            be created.
        url:
            (optional) If compatibility is True, you can pass the base url
            as "<scheme>://<host>:<port>/".
        **kwargs:
            Keyword arguments to pass to requests for the initial
            request retrieving user information.
    """

    if compatibility:
        warnings.warn(
            DeprecationWarning(
                'Support for the old PyLana api will deprecate soon.'
            )
        )
        url = url if url else f'{scheme}://{host}:{port}/'
        return LanaAPI(url, token=token)

    api = LanaAPI2(scheme, host, token, port, application_root, **kwargs)
    api._request = functools.partial(api._request, verify=verify)

    return api
