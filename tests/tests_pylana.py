import json
import unittest

import pandas as pd

from pylana.pylana_v2 import LanaAPI2
from pylana.semantics import create_semantics


class TestLanaAPI2(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('./config.json') as f:
            cls.credentials = json.load(f)
        cls.api = LanaAPI2(**cls.credentials)

    def test_init(self):
        self.api.list_logs()
        self.api.list_user_logs()

    def test_get_log_id(self):
        log_id = self.api.get_log_id('Incident_Management.csv')
        self.assertIsInstance(log_id, str)

        with self.assertRaises(Exception):
            self.api.get_log_id('1212')

    def test_upload_event_log_stream(self):
        log_semantics = create_semantics(['id', 'action', 'start', 'complete', 'number'],
                                         numerical_attributes=['number'])
        case_semantics = create_semantics(['id', 'category', 'age'], numerical_attributes=['age'])

        with open('./data/event-log.csv') as event_stream:
            with open('./data/case-attributes.csv') as case_stream:
                resp = self.api.upload_event_log_stream(
                    log_stream=event_stream,
                    case_stream=case_stream,
                    log_semantics=log_semantics,
                    case_semantics=case_semantics)

        self.assertEqual(resp.status_code, 200)

    def test_upload_event_log(self):
        log_semantics = create_semantics(['id', 'action', 'start', 'complete', 'number'],
                                         numerical_attributes=['number'])
        case_semantics = create_semantics(['id', 'category', 'age'], numerical_attributes=['age'])

        with open('./data/event-log.csv') as f:
            log = f.read()

        with open('./data/case-attributes.csv') as f:
            case_attributes = f.read()

        resp = self.api.upload_event_log(
            name='test-log',
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
            'test-from-df', df_log, df_case, time_format='yyyy-MM-dd HH:mm:ss')

        self.assertEqual(resp.status_code, 200)
