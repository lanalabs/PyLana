from pylana.modules.logs import LogsAPI
from pylana.modules.user_management import get_user_information
from pylana.utils import _create_headers


# TODO: consider certificate passing for TLS
class LanaAPI2(LogsAPI):

    def __init__(self, scheme: str, host: str, token: str, port: int = None):

        self.url = f'{scheme}://{host}' + (f':{port}' if port else '')
        self.headers = _create_headers(token)
        self.user_info = get_user_information(scheme, host, token, port)
        self.userInfo = self.user_info
