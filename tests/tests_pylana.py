import json
import unittest

from pylana.pylana_v2 import LanaAPI2


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

