import io
import json
import os
import re
from typing import List
import zipfile

from requests import Response

from pylana.modules.api import API
from pylana.modules.resources import ResourceAPI
from pylana.utils import expect_json, extract_id, extract_ids
from pylana.utils import handle_response


class ShinyDashboardAPI(ResourceAPI):

    def list_shiny_dashboards(self, **kwargs) -> List[dict]:
        return self.list_resources('shiny-dashboards', **kwargs)

    def get_shiny_dashboard_ids(self, contains: str, **kwargs) -> List[str]:
        return self.get_resource_ids('shiny-dashboards', contains, **kwargs)

    def get_shiny_dashboard_id(self, contains: str, **kwargs) -> str:
        return self.get_resource_id('shiny-dashboards', contains, **kwargs)

    def describe_shiny_dashboard(self, contains: str = None, shiny_dashboard_id: str = None, **kwargs) -> dict:
        """
        get description of shiny dashboard

        Args:
            shiny_dashboard_id: The id of the log, takes precedence over contains
            contains: a regex matching the log's name, matching several names raises an exception

        Returns:

        """
        return self.describe_resource('shiny-dashboards', contains, shiny_dashboard_id, **kwargs)

    # TODO json lacking sharing options
    def create_shiny_dashboard(self, name: str) -> dict:
        return self.create_resource('shiny-dashboards', json={'name': name})

    def upload_shiny_dashboard(self, dashboard_id: str, file: io.IOBase) -> Response:
        return self.post(f"/api/shiny-dashboards/{dashboard_id}/source", files=file)

    def delete_shiny_dashboard(self, shiny_dashboard_id: str, **kwargs):
        return self.delete_resource('shiny-dashboards', shiny_dashboard_id, **kwargs)

    def delete_shiny_dashboards(self, contains: str = None, ids: List[str] = None, **kwargs):
        return self.delete_resources('shiny-dashboards', contains, ids, **kwargs)

    # legacy
    # ------

    def updateDashboardUrl(self, in_file: str, out_file: str, url: str) -> None:
        with open(in_file, 'r+') as f:
            db_string = f.read()
            s = re.sub('lanaUrl <- \".*\"', 'lanaUrl <- ' + '"' + url + '"', db_string)

        with open(out_file, 'w') as out_file:
            out_file.write(s)

    def zipDashboard(self, zip_path: str, dashboard_rmd: str) -> None:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as f:
            f.write(dashboard_rmd, os.path.basename(dashboard_rmd))

    def createShinyDashboard(self, dashboardName: str) -> str:
        body = {"name": dashboardName}
        r = self.post("/api/shiny-dashboards", json=body)
        r_json = json.loads(r.text)
        dashboardId = r_json['id']
        return dashboardId

    def uploadShinyDashboard(self, dashboard: str, dashboardId: str) -> Response:
        file = {'file': open(dashboard, 'rb')}
        return self.post(f"/api/shiny-dashboards/{dashboardId}/source", files=file)

    # Id arguments need to be lists
    def shareDashboard(self, dashboardId:str, userIds: str, projectIds: str, organizationIds: str) -> Response:
        body = {"sharedInformation": {
            "userIds": userIds,
            "projectIds": projectIds,
            "organizationIds": organizationIds
        }}
        return self.patch(f"/api/shiny-dashboards/{dashboardId}", data=body)
