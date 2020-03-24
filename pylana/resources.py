from typing import List, Union

from requests import Response

from .api import API
from .utils import expect_json, extract_id, extract_ids


class ResourceAPI(API):

    @expect_json
    def list_resources(self, kind: str, **kwargs) -> list:
        """
        lists all resources of a kind

        Args:
            kind: resource type name
            **kwargs: arguments passed to requests functions
        """
        return self.get(f'/api/{kind}', **kwargs)

    @extract_ids
    def get_resource_ids(self, kind: str, contains: str, **kwargs) -> List[str]:
        """
        get all resource ids which names are matched by the passed regular expression

        Args:
            kind: resource type name
            contains: a regular expression matched against the log names

        Returns:
            a list of strings representing log ids
        """
        return self.list_resources(kind, **kwargs)

    @extract_id
    def get_resource_id(self, kind: str, contains: str, **kwargs) -> str:
        """
        get id of a resource by its name

        name needs to be unique or an exception is raised
        """
        return self.get_resource_ids(kind, contains, **kwargs)

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

    # resource connections

    def connect_resources(self, dct, **kwargs):
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
