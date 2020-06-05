import json
import unittest

import requests

from pylana.api import get_user_information


class TestGetUserInformation(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('./tests/config.json') as f:
            cls.credentials = json.load(f)

    def test_success(self):
        url = self.credentials['scheme'] + '://' \
            + self.credentials['host'] + ':' \
            + str(self.credentials['port'])
        actual = get_user_information(url, self.credentials['token'])

        expected_keys = [
            'acceptedTerms', 'apiKey', 'apiKeyStatus', 'backendInstanceId',
            'email', 'id', 'organizationId', 'preferences', 'role']

        self.assertCountEqual(actual.keys(), expected_keys)

    def test_failure(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            _ = get_user_information('https://cloud-backend.lanalabs.com',
                                     token='not-a-valid-token ')
