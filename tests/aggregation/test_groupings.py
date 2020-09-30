import unittest

from pylana.aggregation import create_grouping


class TestGroupings(unittest.TestCase):

    def test_create_grouping_by_duration(self):
        actual = create_grouping('byDuration')

        expected = {'type': 'byDuration'}

        self.assertDictEqual(actual, expected)

    def test_create_grouping_by_time(self):
        actual = create_grouping('byMonth', date_type="startDate")

        expected = {'type': 'byMonth', 'dateType': 'startDate',
                    'timeZone': 'Europe/Berlin'}

        self.assertDictEqual(actual, expected)

    def test_create_grouping_by_time_no_date_type(self):
        with self.assertRaises(Exception):
            _ = create_grouping('byMonth')

    def test_create_grouping_by_activity(self):
        actual = create_grouping('byActivity',
                                 activities=['activity1', 'activity2'])

        expected = {'type': 'byActivity',
                    'selectedActivities': ['activity1', 'activity2']}

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

    def test_create_grouping_two_optional_params(self):
        with self.assertRaises(Exception):
            _ = create_grouping('byAttribute',
                                attribute='Country',
                                date_type='startDate')

    def test_create_grouping_three_optional_params(self):
        with self.assertRaises(Exception):
            _ = create_grouping('byAttribute',
                                attribute='Country',
                                date_type='startDate',
                                activities=['activity1', 'activity2'])
