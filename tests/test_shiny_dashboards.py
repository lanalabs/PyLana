import json
import unittest

from pylana import create_api


class TestDashboardAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('./tests/config.json') as f:
            cls.credentials = json.load(f)
        cls.api = create_api(verify=True, **cls.credentials)

    def test_list(self):
        shiny_dashboards = self.api.list_shiny_dashboards()
        self.assertGreaterEqual(len(shiny_dashboards), 1)

    def test_shiny_dashboard_management(self):
        resp_create = self.api.create_shiny_dashboard('pylana-shiny-dashboard')
        resp_describe = self.api.describe_shiny_dashboard('pylana-shiny-dashboard')
        self.assertDictEqual(resp_create, resp_describe)

        id_ = self.api.get_shiny_dashboard_id('pylana-shiny-dashboard')
        resp_delete = self.api.delete_shiny_dashboard(id_)
        self.assertEqual(resp_delete.status_code, 200)

    def test_describe(self):
        shiny_dashboard = self.api.describe_shiny_dashboard('incident-test-.*')
        self.assertEqual(shiny_dashboard.get('name'), 'incident-test-dashboard')

        with self.assertRaises(Exception):
            _ = self.api.describe_shiny_dashboard('never-ever-matches-a-shiny_dashboard')

    def test_get_shiny_dashboard_id(self):
        shiny_dashboard_id = self.api.get_shiny_dashboard_id('incident-test-dashboard')
        self.assertEqual(shiny_dashboard_id, 'fc474eec-922c-4716-a71d-2fe60e53f9b9')

        with self.assertRaises(Exception):
            _ = self.api.get_shiny_dashboard_id('1212')

    def test_share_shiny_dashboard(self):
        id_ = self.api.get_shiny_dashboard_id('incident-test-dashboard')

        actual = self.api.share_shiny_dashboard(id_,
                                                ['b7853d9b-8ca6-4a33-8892-0f172a9aeb09']).json()

        expected = {'sharing': {'numFailures': 0, 'numSuccesses': 1},
                    'unsharing': {'numFailures': 0, 'numSuccesses': 0}}

        self.assertDictEqual(actual, expected)
