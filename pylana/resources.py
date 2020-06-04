"""
resource management api requests
"""

import re
from typing import List, Union

from requests import Response

from pylana.api import API
from pylana.decorators import expect_json


class ResourceAPI(API):

    @expect_json
    def list_resources(self, kind: str, **kwargs) -> list:
        """
        Lists all resources of a kind.

        Args:
            kind:
                A string denoting the resource type.
            **kwargs:
                Keyword arguments passed to requests functions.
        """
        return self.get(f'/api/{kind}', **kwargs)

    def get_resource_ids(self, kind: str, contains: str, **kwargs) -> List[str]:
        """
        Get ids of resource with names are matched by regular expression

        Args:
            kind:
                A string denoting the resource type.
            contains:
                A string denoting a regular expression matched against the log
                names.
            **kwargs:
                Keyword arguments passed to requests functions.

        Returns:
            a list of strings representing log ids
        """
        resources = self.list_resources(kind, **kwargs)
        rc = re.compile(contains)
        return [resource['id'] for resource in resources
                if rc.search(resource['name'])]

    def get_resource_id(self, kind: str, contains: str, **kwargs) -> str:
        """
        Get id of a resource by its name

        name needs to be unique or an exception is raised
        """
        log_ids = self.get_resource_ids(kind, contains, **kwargs)

        try:
            [log_id] = log_ids
        except ValueError as e:
            raise Exception(
                f'Found {len(log_ids)} resources with the pattern {contains}')

        return log_id


    @expect_json
    def describe_resource(self, kind: str, contains: str = None, resource_id: str = None, **kwargs) -> dict:
        """
        get description of resource

        Args:
            kind: resource type name
            resource_id: The id of the log, takes precedence over contains
            contains: a regex matching the resource's name, matching several names raises an exception

        Returns:

        """
        resource_id = resource_id or self.get_resource_id(kind, contains, **kwargs)
        return self.get(f'/api/{kind}/{resource_id}')

    @expect_json
    def create_resource(self, kind: str, json: Union[list, dict, str], **kwargs):
        return self.post(f'/api/{kind}', json=json, **kwargs)

    def delete_resource(self, kind, id_: str, **kwargs) -> Response:
        """
        delete a log by its id
        """
        return self.delete(f'/api/{kind}/{id_}', **kwargs)

    def delete_resources(self, kind: str, contains: str = None, ids: List[str] = None, **kwargs) -> List[Response]:
        """
        deletes one or multiple logs matching the passed regular expression
        """
        ids = ids or self.get_resource_ids(kind, contains, **kwargs)
        return [self.delete_resource(kind, id_) for id_ in ids]

    def connect_resources(self, dct, **kwargs) -> Response:
        return self.post('/api/v2/resource-connections', json=dct, **kwargs)

    def connect_model(self, log_id, model_id, **kwargs):
        dct = {'log_id': log_id, 'model_id': model_id}
        return self.connect_resources(dct, **kwargs)

    def connect_dashboard(self, log_id, dashboard_id, **kwargs):
        dct = {'log_id': log_id, 'dashboard_id': dashboard_id}
        return self.connect_resources(dct, **kwargs)

    def connect_working_schedule(self, log_id, working_schedule_id, **kwargs):
        dct = {'log_id': log_id, 'working_schedule_id': working_schedule_id}
        return self.connect_resources(dct, **kwargs)

    def connect_shiny_dashboard(self, log_id, shiny_dashboard_id, **kwargs) \
            -> Response:
        """
        Connect an shiny dashboard and a log by ids.

        Args:
            log_id:
                A string representing the id of the log.
            shiny_dashboard_id:
                A string representing the id of the shiny dashboard.
            **kwargs:
                Keyword arguments passed to requests functions.
        Returns:
            The requests response of the lana api call.
        """
        dct = {'log_id': log_id, 'shiny_dashboard_id': shiny_dashboard_id}
        return self.connect_resources(dct, **kwargs)
