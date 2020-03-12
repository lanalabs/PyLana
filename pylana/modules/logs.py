import abc
import json
from typing import Union, List

import pandas as pd

from pylana.modules.bases import _API
from pylana.modules.structures import User
from pylana.semantics import create_case_semantics_from_df, create_event_semantics_from_df
from pylana.utils import expect_json
from pylana.utils import handle_response


def prepare_semantics(semantics: Union[str, list]):
    return json.dumps(semantics) if not isinstance(semantics, str) else semantics


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
        return self.get('/api/logs', **kwargs)

    @expect_json
    def list_user_logs(self, **kwargs):
        """
        list all logs owned bt the user

        Args:
            **kwargs: arguments passed to requests functions

        """
        return self.get('/api/users/' + self.user.user_id + '/logs', **kwargs)

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

    def upload_event_log_stream(self, log_stream, log_semantics, case_stream, case_semantics):

        files = {
            'eventCSVFile': (log_stream.name, log_stream.read(), 'text/csv'),
            'caseAttributeFile': (case_stream.name, case_stream.read(), 'text/csv')
        }

        semantics = {
            'eventSemantics': json.dumps(log_semantics),
            'caseSemantics': json.dumps(case_semantics),
            'logName': log_stream.name.split('/').pop(),
            'timeZone': "Europe/Berlin"
        }

        return self.post('/api/logs/csv-case-attributes-event-semantics',
                         files=files, data=semantics)

    def upload_event_log(self, name,
                         log: str, log_semantics: Union[str, List[dict]],
                         case_attributes=None, case_attribute_semantics=None):

        files_required = {
            'eventCSVFile': (name, log, 'text/csv')
        }
        semantics_required = {
            'eventSemantics': prepare_semantics(log_semantics),
            'logName': name,
            'timeZone': "Europe/Berlin"
        }

        files = {
            **files_required,
            **{'caseAttributeFile': (name + '_case_attributes', case_attributes, 'text/csv')}
        } if case_attributes else files_required
        semantics = {
            **semantics_required,
            **{'caseSemantics': prepare_semantics(case_attribute_semantics)}
        } if case_attribute_semantics else semantics_required

        return self.post('/api/logs/csv-case-attributes-event-semantics',
                         files=files, data=semantics)

    @handle_response
    def upload_event_log_df(self,
                            name: str, df_log: pd.DataFrame, df_case: pd.DataFrame, time_format: str):

        df_events, event_semantics = create_event_semantics_from_df(df_log, time_format=time_format)
        df_cases, case_semantics = create_case_semantics_from_df(df_case)

        return self.upload_event_log(name,
                                     log=df_events.to_csv(index=False),
                                     log_semantics=event_semantics,
                                     case_attributes=df_cases.to_csv(index=False),
                                     case_attribute_semantics=case_semantics)


    # legacy methods
    # --------------
    def getUserLogs(self):
        return self.list_user_logs()

    def chooseLog(self, logName):
        userLogs = self.getUserLogs()
        logId = max([x['id'] for x in userLogs if x['name'] == logName])
        return logId
