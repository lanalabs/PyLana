import json
import unittest
from os import path

import pytest

from pylana import create_api


@pytest.mark.skipif(not path.exists('./tests/config_useradmin.json'), 
                    reason='User management can only be tested with' + 
                    ' a user or system admin role.')
class TestUsersAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('./tests/config_useradmin.json') as f:
            cls.credentials_user_admin = json.load(f)
        cls.api_user_admin = create_api(verify=True, **cls.credentials_user_admin)

        with open('./tests/config.json') as f:
            cls.credentials_ranalyst = json.load(f)
        cls.api_r_analyst = create_api(verify=True, **cls.credentials_ranalyst)  
        
    @classmethod
    def tearDownClass(cls) -> None:
        users = cls.api_user_admin.get_all_users()
        for user in users:
            if user['email'] == 'nonexisting@doesnotexistlana.org':
                cls.api_user_admin.delete_user(user['id'])

    def test_list_users(self):
        users = self.api_user_admin.get_all_users()
        self.assertGreaterEqual(len(users), 1)

    def test_user_management(self):
        resp_user_info = self.api_user_admin.get_user_information_by_id(self.api_r_analyst.user.user_id)

        self.assertEqual(resp_user_info['role'], self.api_r_analyst.user.role)

        resp_user_creation = self.api_user_admin.create_user('nonexisting@doesnotexistlana.org',
                                                  'Analyst',
                                                  resp_user_info['organizationId'],
                                                  resp_user_info['backendInstanceId'])

        self.assertEqual(resp_user_creation.status_code, 201)
