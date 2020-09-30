"""
dashboard management api requests
"""

from typing import List

from requests import Response

from pylana.resources import ResourceAPI


class DashboardAPI(ResourceAPI):

    def list_dashboards(self, **kwargs) -> List[dict]:
        """
        List all dashboards available to the user.
        
        Args:
            **kwargs:
                Keyword arguments passed to requests functions.
            
        Returns: 
            A list of strings denoting dashboard names.
        """
        return self.list_resources('v2/dashboards', **kwargs)

    def get_dashboard_ids(self, contains: str = '.*', **kwargs) \
            -> List[str]:
        """
        List dashboard ids with matching names.

        Args:
           contains:  
                A string denoting a regular expression
                matched against the dashboard titles.
            **kwargs: 
                Keyword arguments passed to requests functions.
            
        Returns:
            A list of strings denoting dashboard ids.
        """
        return self.get_resource_ids('v2/dashboards', contains, **kwargs)

    def get_dashboard_id(self, contains: str, **kwargs) -> str:
        """
        Get dashboard id with matching name.

        Args:
            contains:  
                A string denoting a regular expression
                matched against the dashboard name.
            **kwargs: 
                Keyword arguments passed to requests functions.
            
        Returns: 
            A string denoting the dashboard id.

        Raises:
            Exception:
                None or more than one dashboard name matches the
                regular expression.
        """
        return self.get_resource_id('v2/dashboards', contains, **kwargs)

    # TODO json lacks sharing options
    def create_dashboard(self, name: str, items: List[dict], 
                         is_active: bool = False, **kwargs) -> Response:
        """
        Create a dashboard with a list of dashboard items.

        Args:
            name:  
                A string denoting the dashboard name.
            items:
                A list of dicts denoting the dashboard items (referenced as
                charts in LANA Process Mining)
            is_active:
                A boolean denoting if the dashboard should be set
                as the last one selected by the user.
            **kwargs: 
                Keyword arguments passed to requests functions.
            
        Returns:
            The requests response of the lana api call.
        """
        request_data = {'title': name,
                        'items': items,
                        'isActive': is_active}

        return self.create_resource('v2/dashboards/', json=request_data, **kwargs)

    def describe_dashboard(self, contains: str = None,
                           dashboard_id: str = None, **kwargs) -> dict:
        """
        Get dashboard metadata.

        Args:
            contains: 
                A string denoting a regular expression
                matched against the dashboard name. 
                Matching several names raises an exception.
            dashboard_id: 
                A string denoting the id of the dashboard.
            **kwargs: 
                Keyword arguments passed to requests functions.
            
        Returns:
            A dictionary with the dashboard data.
        """
        return self.describe_resource('v2/dashboards', contains, dashboard_id, 
                                      **kwargs)
    
    def describe_dashboard_items(self, contains: str = None,
                                 dashboard_id: str = None, **kwargs) \
            -> List[dict]:
        """
        Get dashboard item metadata.

        Args:
            contains: 
                A string denoting a regular expression
                matched against the dashboard name. 
                Matching several names raises an exception.
            dashboard_id: 
                A string denoting the id of the dashboard.
            **kwargs: 
                Keyword arguments passed to requests functions.
            
        Returns:
            A list with the dashboard items as dicts (items are referenced as
            charts in LANA Process Mining)
        """
        dashboard = self.get_dashboard(contains, dashboard_id, **kwargs)
        
        return dashboard["items"]

    def delete_dashboard(self, dashboard_id: str, **kwargs) \
            -> Response:
        """
        Delete a dashboard by its id.
        
        Args:
            dashboard_id: 
                A string denoting the dashboard.
            **kwargs: 
                Keyword arguments passed to requests functions.

        Returns:
            The requests response of the lana api call.
        """
        return self.delete_resource('v2/dashboards', dashboard_id,
                                    **kwargs)

    def delete_dashboards(self, contains: str = None,
                          ids: List[str] = None, **kwargs) -> \
            List[Response]:
        """
        Delete dashboards with matching names.

        Args:
            contains: 
                A string denoting a regular expression. 
                It is ignored when ids are passed.
            ids: 
                A list of strings denoting dashboard ids.
                
        Returns:
            A list of request responses of the calls to the lana api.
        """
        return self.delete_resources('v2/dashboards', contains, ids,
                                     **kwargs)

    # TODO consider sharing by names
    def share_dashboard(self, dashboard_id: str,
                        user_ids: List[str], organization_ids: List[str],
                        **kwargs) -> Response:
        """
        Share a dashboard with users by ids.

        Args:
            dashboard_id:
                A string denoting the id of the dashboard.
            user_ids:
                A list of strings denoting ids of users to share with.
            organization_ids: 
                A list of strings denoting ids of organizations to share with.

        Returns:
            The requests response of the lana api call.
        """
        body = {
            "sharedInformation": {
                "userIds": user_ids,
                "organizationIds": organization_ids
            }
        }
        return self.patch(f"/api/v2/dashboards/{dashboard_id}", json=body, 
                          **kwargs)

    def connect_dashboard(self, log_id, dashboard_id, **kwargs) \
            -> Response:
        """
        Connect a shiny dashboard with a log by their ids.
        
        Args:
            log_id: 
                A string denoting the id of the log in LANA.
            dashboard_id:
                A string denoting the id of the dashboard.
            **kwargs: 
                Keyword arguments passed to requests functions.

        Returns:
            The requests response of the lana api call.
        """
        dct = {'log_id': log_id, 'dashboard_id': dashboard_id}
        return self.connect_resources(dct, **kwargs)
