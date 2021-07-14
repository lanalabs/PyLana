import json
import unittest

import pandas as pd

from pylana import create_api


class TestAggregationAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('./tests/config.json') as f:
            cls.credentials = json.load(f)
        cls.api = create_api(verify=True, **cls.credentials)

    def assertDataframeEqual(self, a, b, msg, *args, **kwargs):
        try:
            pd.testing.assert_frame_equal(a, b, *args, **kwargs)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def setUp(self):
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    def test_aggregate_attribute_time_groupings(self):
        log_id = self.api.get_log_id('Incident_Management.csv')

        expected_df = pd.DataFrame({'caseCount': [891, 557, 363, 189],
                                    'Country': ['Germany', 'Austria', 'Netherlands', 'Switzerland'],
                                    'frequency': [891, 557, 363, 189],
                                    'byMonth': ['Jan 2016', 'Jan 2016', 'Jan 2016', 'Jan 2016']})

        resp_aggregate_df = self.api.aggregate(log_id=log_id,
                                               metric='frequency',
                                               grouping='byAttribute',
                                               attribute='Country',
                                               secondary_grouping='byMonth',
                                               secondary_date_type='startDate')

        self.assertEqual(expected_df, resp_aggregate_df)

    def test_aggregate_numeric_attribute_metrics(self):
        log_id = self.api.get_log_id('Incident_Management.csv')

        expected_df = pd.DataFrame({'caseCount': [2000],
                                    None: ['No grouping'],
                                    'Cost': [8536000]})

        resp_aggregate_df = self.api.aggregate(log_id=log_id,
                                               metric='Cost',
                                               aggregation_function='sum')

        self.assertEqual(expected_df, resp_aggregate_df)

    def test_aggregate_sorting_order(self):
        log_id = self.api.get_log_id('Incident_Management.csv')

        expected_df = pd.DataFrame({'caseCount': [109, 295, 57, 610, 929],
                                    'Classification': ['Backup', 'Citrix', 'Intranet', 'Mail', 'SAP'],
                                    'duration': [23770458.715596333, 63067525.423728816, 22307368.421052627,
                                                 27052327.868852418, 49583186.221743822]})

        resp_aggregate_df = self.api.aggregate(log_id=log_id,
                                               metric='duration',
                                               grouping='byAttribute',
                                               attribute='Classification',
                                               aggregation_function='mean',
                                               value_sorting='alphabetic',
                                               sorting_order='ascending')

        self.assertEqual(expected_df, resp_aggregate_df)

    def test_aggregate_tfs_max_amount(self):
        log_id = self.api.get_log_id('Incident_Management.csv')

        expected_df = pd.DataFrame({'caseCount': [1080, 978, 762, 368, 281, 142, 140, 139, 133, 1677],
                                    'byHourOfDay': ['13', '12', '14', '11', '15', '23', '16', '6', '4', 'Other'],
                                    'Cost': [146000, 120000, 162000, 176000, 109000, 94000, 64000, 168000,
                                             149000, 2223000]})

        trace_filter_sequence = [{'pre': 'Incident classification',
                                  'succ': 'Functional escalation',
                                  'direct': False,
                                  'useDuration': False,
                                  'type': 'followerFilter',
                                  'inverted': False}]

        resp_aggregate_df = self.api.aggregate(log_id=log_id,
                                               metric='Cost',
                                               aggregation_function='sum',
                                               grouping='byHourOfDay',
                                               date_type='startDate',
                                               max_amount_attributes=9,
                                               trace_filter_sequence=trace_filter_sequence,
                                               values_from='allEvents')

        self.assertEqual(expected_df, resp_aggregate_df)

    def test_boxplot_stats(self):
        log_id = self.api.get_log_id('Incident_Management.csv')

        expected_df = pd.DataFrame({'min': [500, 500, 500, 500, 500],
                                    'max': [21000, 23000, 1000, 1000, 1000],
                                    'median': [500, 15000, 1000, 500, 500],
                                    'p25': [500, 500, 500, 500, 500],
                                    'p75': [2000, 20000, 1000, 500, 500]},
                                   index=pd.Series(['SAP', 'Mail', 'Citrix', 'Backup', 'Intranet'],
                                                   name='Classification'))

        resp_boxplot_df = self.api.boxplot_stats(log_id=log_id,
                                                 metric='Cost',
                                                 grouping='byAttribute',
                                                 attribute='Classification')

        self.assertEqual(expected_df, resp_boxplot_df)

    def test_by_activity_grouping(self):
        """The purpose of this test is to check if no acitvities are provided, the aggregation is based on all activities.
           This was previously not possible with pylana."""
           
        log_id = self.api.get_log_id('Incident_Management.csv')

        activities = ['Initial diagnosis', 'Incident closure', 'Incident classification',
                      'Incident logging', 'Resolution and recovery',
                      'Investigation and diagnosis', 'Functional escalation']

        df_a = self.api.aggregate(log_id=log_id, metric="frequency",grouping= "byActivity", values_from= "allEvents")
        df_b = self.api.aggregate(log_id=log_id, metric="frequency",grouping= "byActivity", values_from= "allEvents", activities=activities)

        self.assertEqual(df_a, df_b)