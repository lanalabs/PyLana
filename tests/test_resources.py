import json
import unittest

from pylana import create_api


class TestDashboardAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        with open('./tests/config.json') as f:
            cls.credentials = json.load(f)
        cls.api = create_api(verify=True, **cls.credentials)

    def get_organisations_shared_with(self, *args, **kwargs):
        return self.api.describe_resource(
                *args,
                **kwargs
            ).get(
            "sharedInformation", dict()
        ).get(
            "organizationIds", dict()
        )

    def test_share_resource(self):
        rid = self.api.get_resource_id(
            kind="v2/dashboards",
            contains="INCIDENT.*"
        )
        self.assertEqual(
            self.get_organisations_shared_with(
                "v2/dashboards",
                resource_id=rid
            ),
            []
        )

        _ = self.api.share_resource("dashboards", resource_id=rid)
        self.assertEqual(
            self.get_organisations_shared_with(
                "v2/dashboards",
                resource_id=rid
            ),
            [self.api.user.organization_id]
        )

        _ = self.api.unshare_resource("dashboards", resource_id=rid)
        self.assertEqual(
            self.get_organisations_shared_with(
                "v2/dashboards",
                resource_id=rid
            ),
            []
        )
