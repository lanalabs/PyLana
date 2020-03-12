import abc

from pylana.utils import expect_json
from pylana.modules.bases import _API


class LogsAPI(_API, abc.ABC):

    headers = dict()
    userInfo = dict()
    user_info = dict()
    url = ''

    @expect_json
    def list_logs(self, **kwargs):
        """
        lists all logs that are available to the user
        """

        # resp = requests.get(url=self.url + '/api/logs', headers=self.headers)
        resp = self.get(url=self.url + '/api/logs', **kwargs)
        resp.raise_for_status()

        return resp

    @expect_json
    def list_user_logs(self, **kwargs):
        resp = self.get(url=self.url + '/api/users/' + self.user_info['id'] + '/logs', **kwargs)
        resp.raise_for_status()

        return resp

    # legacy methods
    # --------------
    def getUserLogs(self):
        return self.list_user_logs()

