import json
import unittest

import requests

from pylana.api import get_user_information
from pylana import create_api

class TestUsersAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('./tests/admin_config.json') as f:
            cls.credentials = json.load(f)
        cls.api = create_api(verify=True, **cls.credentials)

    def test_user_by_token_success(self):
        url = self.credentials['scheme'] + '://' \
            + self.credentials['host'] + ':' \
            + str(self.credentials['port'])
        actual = get_user_information(url, self.credentials['token'])

        expected_keys = [
            'acceptedTerms', 'apiKey', 'apiKeyStatus', 'backendInstanceId',
            'email', 'id', 'organizationId', 'preferences', 'role']

        self.assertCountEqual(actual.keys(), expected_keys)

    def test_user_by_token_failure(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            _ = get_user_information('https://cloud-backend.lanalabs.com',
                                     token='not-a-valid-token ')

    def test_list_users(self):
        users = self.api.get_all_users()
        self.assertGreaterEqual(len(users), 1)

    def test_user_management(self):
        resp_user_info = self.api.get_user_information_by_id('e44e8b55-1b28-4db7-9396-6acd4e94ee2a')

        self.assertEqual(resp_user_info['role'], 'UserAdmin')

        resp_user_creation = self.api.create_user('nonexisting@doesnotexistlana.org',
                                                  'Analyst',
                                                  resp_user_info['organizationId'],
                                                  resp_user_info['backendInstanceId'])

        self.assertEqual(resp_user_creation.status_code, 200)

        resp_delete_user = self.api.delete_user(resp_user_creation.json()['id'])

        self.assertEqual(resp_delete_user.status_code, 200)
