import json
import unittest

from pylana import create_api


class TestDashboardAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('./tests/config.json') as f:
            cls.credentials = json.load(f)
        cls.api = create_api(verify=True, **cls.credentials)

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
        resp_get = self.api.get_dashboard('pylana-dashboard')
        self.assertDictEqual(resp_create, resp_get)

        id_ = self.api.get_dashboard_id('pylana-dashboard')
        resp_delete = self.api.delete_dashboard(id_)
        self.assertEqual(resp_delete.status_code, 200)

    def test_get_dashboard(self):
        dashboard = self.api.get_dashboard('pylana-test-log-.*')
        self.assertEqual(dashboard.get('title'), 'pylana-test-log-from-df')

        with self.assertRaises(Exception):
            _ = self.api.get_dashboard('never-ever-matches-a-dashboard')

    def test_get_dashboard_id(self):
        dashboard_id = self.api.get_dashboard_id('pylana-test-log-from-df')
        self.assertEqual(dashboard_id, '529de59d-6f3d-4e3f-988a-86cd9afe6bb8')

        with self.assertRaises(Exception):
            _ = self.api.get_dashboard_id('1212')
