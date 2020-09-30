import unittest

from pylana.aggregation import create_metric


class TestMetrics(unittest.TestCase):

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
                    'aggregationFunction': {'type': 'percentile',
                                            'percentile': 12}}

        self.assertDictEqual(actual, expected)

    def test_create_metric_attribute(self):
        with self.assertRaises(Exception):
            _ = create_metric('Cost')

    def test_create_metric_attribute_with_agg_function(self):
        actual = create_metric('Cost', 'sum')

        expected = {'type': 'attribute', 'attribute': 'Cost',
                    'aggregationFunction': 'sum'}

        self.assertDictEqual(actual, expected)

    def test_create_metric_attribute_with_percentile(self):
        actual = create_metric('Cost', aggregator=None, percentile=12)

        expected = {'type': 'attribute',
                    'attribute': 'Cost',
                    'aggregationFunction': {'type': 'percentile',
                                            'percentile': 12}}

        self.assertDictEqual(actual, expected)

    def test_create_metric_attribute_with_agg_function_and_percentile(self):
        with self.assertRaises(Exception):
            _ = create_metric('Cost', aggregator='sum', percentile=12)
