"""
shiny dashboard management api requests
"""


import io
import json
import os
import re
import zipfile
from typing import List

from requests import Response

from .resources import ResourceAPI


class ShinyDashboardAPI(ResourceAPI):

    def list_shiny_dashboards(self, **kwargs) -> List[dict]:
        """
        list all shiny dashboards available to the user
        """
        return self.list_resources('shiny-dashboards', **kwargs)

    def get_shiny_dashboard_ids(self, contains: str, **kwargs) -> List[str]:
        """
        list of shiny dashboard ids with matching names

        Args:
            contains: a python re module regular expression
        """
        return self.get_resource_ids('shiny-dashboards', contains, **kwargs)

    def get_shiny_dashboard_id(self, contains: str, **kwargs) -> str:
        """
        return shiny dashboard id with matching name

        raises exception if none ore more than one shiny dashboard matches

        Args:
            contains: a python re module regular expression
        """
        return self.get_resource_id('shiny-dashboards', contains, **kwargs)

    def describe_shiny_dashboard(self, contains: str = None, shiny_dashboard_id: str = None, **kwargs) -> dict:
        """
        get shiny dashboard metadata

        Args:
            shiny_dashboard_id: The id of the log, takes precedence over contains
            contains: a regex matching the log's name, matching several names raises an exception
        """
        return self.describe_resource('shiny-dashboards', contains, shiny_dashboard_id, **kwargs)

    # TODO json lacks sharing options
    def create_shiny_dashboard(self, name: str, **kwargs) -> dict:
        """
        create a named shiny dashboard
        Args:
            name: a string denoting the dashboards name

        Returns:
            a dictionary representing the shiny dashboard metadata
        """
        return self.create_resource('shiny-dashboards', json={'name': name}, **kwargs)

    def upload_shiny_dashboard(self, dashboard_id: str, file: io.IOBase, **kwargs) -> Response:
        """
        upload and replace shiny dashboard source code

        example usage:

            with open('./path_to_dashboard/dashboard.zip', r) as f:
                instance.upload_shiny_dashboard(<dashboard_id>, f)

        Args:
            dashboard_id: a string denoting the shiny dashboard
            file: a io.Base pointing to the zipped dashboard code

        Returns:
            the response of the api call
        """
        return self.post(f"/api/shiny-dashboards/{dashboard_id}/source", files=file, **kwargs)

    def delete_shiny_dashboard(self, shiny_dashboard_id: str, **kwargs):
        """
        delete a shiny dashboard by its id
        """
        return self.delete_resource('shiny-dashboards', shiny_dashboard_id, **kwargs)

    def delete_shiny_dashboards(self, contains: str = None, ids: List[str] = None, **kwargs):
        """
        delete shiny dashboards by id list of name matching

        Args:
            contains: a python re module regular expression, ignored when ids are passed
            ids: a list of strings representing shiny dashboard ids, takes precedence over contains
        """
        return self.delete_resources('shiny-dashboards', contains, ids, **kwargs)

    # TODO consider sharing by names
    def share_shiny_dashboard(self, shiny_dashboard_id: str,
                              user_ids: List[str], project_ids: List[str], organization_ids: str, **kwargs) -> Response:
        """
        share a shiny dashboard with users by ids

        Args:
            shiny_dashboard_id: a string representing the id of the shiny dashboard
            user_ids: a list of strings representing ids of users to share with
            project_ids: a list of strings representing ids of projects to share with
            organization_ids: a list of strings representing ids of organizations share with
        """
        body = {"sharedInformation": {
            "userIds": user_ids,
            "projectIds": project_ids,
            "organizationIds": organization_ids
        }}
        return self.patch(f"/api/shiny-dashboards/{shiny_dashboard_id}", data=body, **kwargs)

    def connect_shiny_dashboard(self, log_id, shiny_dashboard_id, **kwargs):
        """
        connect an shiny dashboard with a log by their ids
        """
        dct = {'log_id': log_id, 'shiny_dashboard_id': shiny_dashboard_id}
        return self.connect_resources(dct, **kwargs)

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
