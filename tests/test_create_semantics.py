import unittest

import pandas as pd

from pylana.utils import create_semantics, create_event_semantics_from_df, create_case_semantics_from_df


# TODO: Test column ordering and indexing
class TestCreateSemantics(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.columns = ['id', 'action', 'start', 'complete', 'number']

    def test_create_semantics(self):
        actual = create_semantics(self.columns, 'id', 'action', 'start', 'complete', ['number'])

        expected = [{"format": None, "idx": 0, "name": "id", "semantic": "Case ID"},
                    {"format": None, "idx": 1, "name": "action", "semantic": "Action"},
                    {"format": "yyyy-MM-dd HH:mm:ss", "idx": 2, "name": "start", "semantic": "Start"},
                    {"format": "yyyy-MM-dd HH:mm:ss", "idx": 3, "name": "complete", "semantic": "Complete"},
                    {"format": None, "idx": 4, "name": "number", "semantic": "NumericAttribute"}]

        msg = 'failed to extract semantics from columns'
        self.assertCountEqual(actual, expected, msg)

    def test_create_event_semantics_from_df(self):
        records = [
            {'Case_ID': 1, 'Action': 'A', 'Start': '2020-02-02 12:00:00', 'Count': 1.0, 'Category': 'A'},
            {'Case_ID': 1, 'Action': 'B', 'Start': '2020-02-02 13:00:00', 'Count': 1.1, 'Category': 'B'},
            {'Case_ID': 2, 'Action': 'A', 'Start': '2020-02-02 12:30:00', 'Count': 1.2, 'Category': 'C'},
            {'Case_ID': 3, 'Action': 'C', 'Start': '2020-02-02 13:30:00', 'Count': 1.3, 'Category': 'D'}
        ]
        df_log = pd.DataFrame(records)\
            .astype({'Case_ID': str, 'Action': str, 'Start': 'datetime64[ns]', 'Count': float, 'Category': str})\
            .loc[:, ['Action', 'Case_ID', 'Start', 'Count', 'Category']]
        expected = [{'format': None, 'idx': 0, 'name': 'Action',
                     'semantic': 'Action'},
                    {'format': None, 'idx': 1, 'name': 'Case ID',
                     'semantic': 'Case ID'},
                    {'format': "yyyy-MM-dd'T'HH:mm:ss.SSSSSS",
                     'idx': 2,
                     'name': 'Start',
                     'semantic': 'Start'},
                    {'format': None, 'idx': 3, 'name': 'Count',
                     'semantic': 'NumericAttribute'},
                    {'format': None,
                     'idx': 4,
                     'name': 'Category',
                     'semantic': 'CategorialAttribute'}
                    ]

        semantics_res = create_event_semantics_from_df(df_log)

        msg = 'failed to derive semantics from pandas data frame'
        self.assertCountEqual(semantics_res, expected, msg)

    def test_create_case_semantics_from_df(self):
        records = [
            {'Case_ID': 1, 'Numeric': 1000, 'Categorical': 'A', 'Boolean': True},
            {'Case_ID': 2, 'Numeric': 3000, 'Categorical': 'C', 'Boolean': False},
            {'Case_ID': 3, 'Numeric': 2000, 'Categorical': 'D', 'Boolean': True},
        ]
        df_case = pd.DataFrame(records)\
            .astype({'Case_ID': str, 'Numeric': int, 'Categorical': str})
        expected = [
            {'format': None, 'idx': 0, 'name': 'Case ID',
             'semantic': 'Case ID'},
            {'format': None, 'idx': 1, 'name': 'Numeric',
             'semantic': 'NumericAttribute'},
            {'format': None, 'idx': 2, 'name': 'Categorical',
             'semantic': 'CategorialAttribute'},
            {'format': None, 'idx': 3, 'name': 'Boolean',
             'semantic': 'CategorialAttribute'}
                    ]

        msg = 'failed to derive case semantics from pandas data frame: '
        semantics_res = create_case_semantics_from_df(df_case)
        self.assertCountEqual(semantics_res, expected, msg + 'wrong type semantics')
