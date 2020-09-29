import unittest

import pandas as pd

from pylana.utils_aggregation import create_metric, create_grouping


class TestAggregationFunctions(unittest.TestCase):

    def test_create_metric_frequency(self):
        actual = create_metric('frequency')

        expected = {'type': 'frequency'}

        self.assertDictEqual(actual, expected)

    def test_create_metric_frequency_with_agg_function(self):
        actual = create_metric('frequency', 'sum')

        expected = {'type': 'frequency'}

        self.assertDictEqual(actual, expected)

    def test_create_metric_frequency_with_percentile(self):
        actual = create_metric('frequency', None, 12)

        expected = {'type': 'frequency'}

        self.assertDictEqual(actual, expected)

    def test_create_metric_duration(self):
        with self.assertRaises(Exception):
            _ = create_metric('duration')

    def test_create_metric_duration_with_agg_function(self):
        actual = create_metric('duration', 'sum')

        expected = {'type': 'duration', 'aggregationFunction': 'sum'}

        self.assertDictEqual(actual, expected)

    def test_create_metric_duration_with_percentile(self):
        actual = create_metric('duration', None, 12)

        expected = {'type': 'duration',
                    'aggregationFunction': {'type': 'percentile', 'percentile': 12}}

        self.assertDictEqual(actual, expected)

    def test_create_metric_attribute(self):
        with self.assertRaises(Exception):
            _ = create_metric('Cost')

    def test_create_metric_attribute_with_agg_function(self):
        actual = create_metric('Cost', 'sum')

        expected = {'type': 'attribute', 'attribute': 'Cost', 'aggregationFunction': 'sum'}

        self.assertDictEqual(actual, expected)

    def test_create_metric_attribute_with_percentile(self):
        actual = create_metric('Cost', aggregator=None, percentile=12)

        expected = {'type': 'attribute',
                    'attribute': 'Cost',
                    'aggregationFunction': {'type': 'percentile', 'percentile': 12}}

        self.assertDictEqual(actual, expected)

    def test_create_grouping_by_duration(self):
        actual = create_grouping('byDuration')

        expected = {'type': 'byDuration'}

        self.assertDictEqual(actual, expected)

    def test_create_grouping_by_time(self):
        actual = create_grouping('byMonth', date_type="startDate")

        expected = {'type': 'byMonth', 'dateType': 'startDate', 'timeZone': 'Europe/Berlin'}

        self.assertDictEqual(actual, expected)

    def test_create_grouping_by_time_no_date_type(self):
        with self.assertRaises(Exception):
            _ = create_grouping('byMonth')

    def test_create_grouping_by_activity(self):
        actual = create_grouping('byActivity', activities=['activity1', 'activity2'])

        expected = {'type': 'byActivity', 'selectedActivities': ['activity1', 'activity2']}

        self.assertDictEqual(actual, expected)

    def test_create_grouping_by_attribute(self):
        actual = create_grouping('byAttribute', attribute='Country')

        expected = {'type': 'byAttribute', 'attribute': 'Country'}

        self.assertDictEqual(actual, expected)

    def test_create_grouping_by_attribute_no_attribute(self):
        with self.assertRaises(Exception):
            _ = create_grouping('byAttribute')

    def test_create_grouping_invalid_grouping(self):
        with self.assertRaises(Exception):
            _ = create_grouping('invalid_grouping')
