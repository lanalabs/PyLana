import json
import unittest

from pylana.pylana_v2 import LanaAPI2


class TestLanaAPI2(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('./config.json') as f:
            cls.credentials = json.load(f)

    def test_init(self):
        api = LanaAPI2(**self.credentials)

        api.list_logs()
        api.list_user_logs()
