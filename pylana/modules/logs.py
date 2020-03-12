import abc

from pylana.utils import expect_json
from pylana.modules.bases import _API
from pylana.modules.structures import User


class LogsAPI(_API, abc.ABC):

    headers: dict
    userInfo: dict
    user: User
    url: str

    @expect_json
    def list_logs(self, **kwargs):
        """
        lists all logs that are available to the user

        Args:
            **kwargs: arguments passed to requests functions
        """
        return self.get(url=self.url + '/api/logs', **kwargs)

    @expect_json
    def list_user_logs(self, **kwargs):
        """
        list all logs owned bt the user

        Args:
            **kwargs: arguments passed to requests functions

        """
        return self.get(url=self.url + '/api/users/' + self.user.user_id + '/logs', **kwargs)

    def get_log_id(self, log_name: str) -> str:
        """
        get id of a log by its name

        name needs to be unique or an exception is raised
        """

        logs_matching = [log['id'] for log in self.list_logs() if log['name'] == log_name]

        try:
            [log_id] = logs_matching
        except ValueError as e:
            raise Exception(f'Found {len(logs_matching)} logs with the name {log_name}')

        return log_id



    # legacy methods
    # --------------
    def getUserLogs(self):
        return self.list_user_logs()

