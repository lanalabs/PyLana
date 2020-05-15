import json
import unittest

import pandas as pd

from pylana import create_api
from pylana.utils import create_semantics


class TestLogsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('./tests/config.json') as f:
            cls.credentials = json.load(f)
        cls.api = create_api(verify=True, **cls.credentials)

    def test_list(self):
        _ = self.api.list_logs()
        _ = self.api.list_user_logs()
        _ = self.api.get('/invalid-route')

    def test_describe(self):
        log = self.api.describe_log('Incident.*')
        self.assertIsInstance(log.get('id'), str)

        with self.assertRaises(Exception):
            _ = self.api.describe_log('never-ever-matches-a-log')

    def test_get_log_id(self):
        log_id = self.api.get_log_id('Incident_Management.csv')
        self.assertIsInstance(log_id, str)

        with self.assertRaises(Exception):
            self.api.get_log_id('1212')

    def test_request_event_csv(self):
        log_id = self.api.get_log_id('Incident_Management.csv')
        resp = self.api.request_event_csv(log_id)
        self.assertEqual(resp.status_code, 200, 'Failed to retrieve existing log')

        mining_request = {
            'activityExclusionFilter': [],
            'includeHeader': True,
            'includeLogId': False,
            'logId': log_id,
            'edgeThreshold': 1,
            'traceFilterSequence': [],
            'exportCaseAttributes': True,
            'onlyColumns': ["Case ID", "Action"],
            'runConformance': False}
        resp = self.api.request_event_csv(log_id, mining_request=mining_request)
        self.assertEqual(resp.status_code, 200, 'Failed to retrieve existing log with mining request')

        resp = self.api.request_event_csv('never-ever-matches-a-log-id')
        self.assertNotEqual(resp.status_code, 200, 'Succeeded to retrieve a non-existent log')

    def test_get_event_log(self):
        log_id = self.api.get_log_id('Incident_Management.csv')
        log = self.api.get_event_log(log_id=log_id)
        self.assertGreater(len(log), 0)

        mining_request = {
            'activityExclusionFilter': [],
            'includeHeader': True,
            'includeLogId': False,
            'logId': log_id,
            'edgeThreshold': 1,
            'traceFilterSequence': [],
            'exportCaseAttributes': True,
            'onlyColumns': ["Case ID", "Action"],
            'runConformance': False}
        log = self.api.get_event_log(log_id=log_id, mining_request=mining_request)
        self.assertGreater(len(log), 0, 'Failed to retrieve existing log')

        log = self.api.get_event_log(log_id='never-ever-matches-a-log-id')
        self.assertTrue(log.empty and log.columns.empty, 'Retrieving non-existent log led to non-empty dataframe')

    def test_upload_event_log_stream(self):
        log_semantics = create_semantics(['id', 'action', 'start', 'complete', 'number'],
                                         numerical_attributes=['number'])
        case_semantics = create_semantics(['id', 'category', 'age'], numerical_attributes=['age'])

        with open('./tests/data/pylana-event-log.csv') as event_stream:
            with open('./tests/data/pylana-case-attributes.csv') as case_stream:
                resp = self.api.upload_event_log_stream(
                    log=event_stream,
                    case=case_stream,
                    log_semantics=log_semantics,
                    case_semantics=case_semantics)

        self.assertEqual(resp.status_code, 200)

    def test_upload_event_log(self):
        log_semantics = create_semantics(['id', 'action', 'start', 'complete', 'number'],
                                         numerical_attributes=['number'])
        case_semantics = create_semantics(['id', 'category', 'age'], numerical_attributes=['age'])

        with open('./tests/data/pylana-event-log.csv') as f:
            log = f.read()

        with open('./tests/data/pylana-case-attributes.csv') as f:
            case_attributes = f.read()

        resp = self.api.upload_event_log(
            name='pylana-test-log',
            log=log,
            case_attributes=case_attributes,
            log_semantics=log_semantics,
            case_attribute_semantics=case_semantics)

        self.assertEqual(resp.status_code, 200)

    def test_upload_event_log_from_df(self):
        
        records = [
            {'Case_ID': 1, 'Action': 'A', 'Start': '2020-02-02 12:00:00', 'Event_Numeric': 1.0, 'Event_Category': 'A1'},
            {'Case_ID': 1, 'Action': 'B', 'Start': '2020-02-02 13:00:00', 'Event_Numeric': 1.1, 'Event_Category': 'B1'},
            {'Case_ID': 2, 'Action': 'A', 'Start': '2020-02-02 12:30:00', 'Event_Numeric': 1.2, 'Event_Category': 'C1'},
            {'Case_ID': 3, 'Action': 'C', 'Start': '2020-02-02 13:30:00', 'Event_Numeric': 1.3, 'Event_Category': 'D1'}
        ]
        df_log = pd.DataFrame(records)\
            .astype({'Case_ID': str, 'Action': str, 'Start': 'datetime64[ns]', 'Event_Numeric': int, 'Event_Category': str})\
            .loc[:, ['Action', 'Case_ID', 'Start', 'Event_Numeric', 'Event_Category']]

        records = [
            {'Case_ID': 1, 'Case_Numeric': 1000, 'Case_Category': 'A2'},
            {'Case_ID': 2, 'Case_Numeric': 3000, 'Case_Category': 'C2'},
            {'Case_ID': 3, 'Case_Numeric': 2000, 'Case_Category': 'D2'}
        ]
        df_case = pd.DataFrame(records)\
            .astype({'Case_ID': str, 'Case_Numeric': int, 'Case_Category': str})

        resp = self.api.upload_event_log_df(
            'pylana-test-log-from-df', df_log, df_case, time_format='yyyy-MM-dd HH:mm:ss')

        self.assertEqual(resp.status_code, 200)

        log_id = resp.json()['logId']

        resp_appended = self.api.append_events_df(log_id, df_log, time_format='yyyy-MM-dd HH:mm:ss')
        self.assertEqual(resp_appended.status_code, 200)

        resp_appended = self.api.append_case_attributes_df(log_id, df_case)
        self.assertEqual(resp_appended.status_code, 200)

    def test_log_sharing(self):
        log_id = self.api.get_log_id('Incident.*')
        resp_share = self.api.share_log(log_id)
        resp_share.raise_for_status()
        # self.assertEqual(resp_share.status_code, 201)

        resp_unshare = self.api.unshare_log(log_id)
        resp_unshare.raise_for_status()
        # self.assertEqual(resp_unshare.status_code, 200)

    # the z character ensures that this is the last test to be executed
    def test_z_delete_logs(self):
        resps = self.api.delete_logs('pylana.*')
        for status_code in [r.status_code for r in resps]:
            self.assertEqual(status_code, 200)
