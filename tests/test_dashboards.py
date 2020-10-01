import json
import unittest

from pylana import create_api


class TestDashboardAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('./tests/config.json') as f:
            cls.credentials = json.load(f)
        cls.api = create_api(verify=True, **cls.credentials)
       
    @classmethod
    def tearDownClass(cls) -> None:
        id_ = cls.api.get_dashboard_id('pylana-dashboard')
        cls.api.delete_dashboard(id_)

        test_dashboard_id_ = cls.api.get_dashboard_id('incident-test-dashboard')
        cls.api.unshare_dashboard(test_dashboard_id_,
                                  [cls.api.user.organization_id])
        
    def test_list_dashboards(self):
        dashboards = self.api.list_dashboards()
        self.assertGreaterEqual(len(dashboards), 1)

    def test_dashboard_management(self):
        items = [{'cols': 6,
                  'itemId': 'c14ae044-cef4-4fd0-a588-036881e83853',
                  'rows': 5,
                  'settingsObj': {'metric': {'attribute': 'Cost', 'type': 'attributeValue'},
                  'valuesFrom': {'type': 'allCases'}},
                  'subtype': 'histogram',
                  'title': 'hist',
                  'type': 'chart',
                  'x': 0,
                  'y': 0}]
        resp_create = self.api.create_dashboard('pylana-dashboard', items)
        resp_get = self.api.describe_dashboard('pylana-dashboard')
        self.assertDictEqual(resp_create, resp_get)

    def test_get_dashboard(self):
        dashboard = self.api.describe_dashboard('incident.*')
        self.assertEqual(dashboard.get('title'), 'incident-test-dashboard')

        with self.assertRaises(Exception):
            _ = self.api.get_dashboard('never-ever-matches-a-dashboard')

    def test_get_dashboard_id(self):
        test_dashboard_id = self.api.get_dashboard_id('incident-test-dashboard')
        self.assertIsInstance(test_dashboard_id, str)

        with self.assertRaises(Exception):
            _ = self.api.get_dashboard_id('never-ever-matches-a-dashboard')

    def test_share_dashboard(self):
        id_ = self.api.get_dashboard_id('incident-test-dashboard')

        actual = self.api.share_dashboard(id_,
                                          [self.api.user.organization_id]).json()

        expected = {'sharing': {'numFailures': 0, 'numSuccesses': 1},
                    'unsharing': {'numFailures': 0, 'numSuccesses': 0}}

        self.assertDictEqual(actual, expected)
