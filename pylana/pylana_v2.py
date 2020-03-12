from pylana.modules.logs import LogsAPI
from pylana.modules.structures import User
from pylana.modules.user_management import get_user_information
from pylana.utils import _create_headers


# TODO: consider certificate passing for TLS
class LanaAPI2(LogsAPI):

    def __init__(self, scheme: str, host: str, token: str, port: int = None):

        self.url = f'{scheme}://{host}' + (f':{port}' if port else '')
        user_info = get_user_information(scheme, host, token, port)
        self.user = User(user_id=user_info.get('id'),
                         organization_id=user_info.get('organizationId'),
                         api_key=user_info.get('apiKey'),
                         role=user_info.get('role'))

        # required for legacy methods
        self.userInfo = user_info
        self.headers = _create_headers(token)
