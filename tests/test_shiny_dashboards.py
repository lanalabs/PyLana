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
        id_ = cls.api.get_shiny_dashboard_id('pylana-shiny-dashboard')
        _ = cls.api.delete_shiny_dashboard(id_)

        test_shiny_dashboard_id_ = cls.api.get_shiny_dashboard_id('incident-test-shiny-dashboard')
        _ = cls.api.unshare_shiny_dashboard(test_shiny_dashboard_id_,
                                            [cls.api.user.organization_id])

    def test_list(self):
        shiny_dashboards = self.api.list_shiny_dashboards()
        self.assertGreaterEqual(len(shiny_dashboards), 1)

    def test_shiny_dashboard_management(self):
        resp_create = self.api.create_shiny_dashboard('pylana-shiny-dashboard')
        resp_describe = self.api.describe_shiny_dashboard('pylana-shiny-dashboard')
        self.assertDictEqual(resp_create, resp_describe)

    def test_describe(self):
        shiny_dashboard = self.api.describe_shiny_dashboard('incident-test-.*')
        self.assertEqual(shiny_dashboard.get('name'), 'incident-test-shiny-dashboard')

        with self.assertRaises(Exception):
            _ = self.api.describe_shiny_dashboard('never-ever-matches-a-shiny_dashboard')

    def test_get_shiny_dashboard_id(self):
        shiny_dashboard_id = self.api.get_shiny_dashboard_id('incident-test-shiny-dashboard')
        self.assertIsInstance(shiny_dashboard_id, str)

        with self.assertRaises(Exception):
            _ = self.api.get_shiny_dashboard_id('1212')

    def test_share_shiny_dashboard(self):
        shiny_dashboard_id = self.api.get_shiny_dashboard_id('incident-test-shiny-dashboard')

        actual = self.api.share_shiny_dashboard(shiny_dashboard_id,
                                                [self.api.user.organization_id]).json()

        expected = {'sharing': {'numFailures': 0, 'numSuccesses': 1},
                    'unsharing': {'numFailures': 0, 'numSuccesses': 0}}

        self.assertDictEqual(actual, expected)
