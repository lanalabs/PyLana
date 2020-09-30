"""
user management api requests functions and methods
"""

from requests import Response

from pylana.resources import ResourceAPI


class UsersAPI(ResourceAPI):

    def create_user(self, email: str, role: str, organization_id: str,
                    backend_instance_id: str, language: str = 'en-US',
                    **kwargs) -> Response:
        """Create a new user in an organization. Admin priviliges necessary.

        This function only works for cloud deployments as on-premise
        deployments expect an encrypted password in the request body.

        Args:
            email:
                A string denoting the e-mail-address of the new user.
            role:
                A string denoting the role of the new user. Has to be one
                of ['Viewer', 'Analyst', 'RAnalyst', 'UserAdmin', 'SuperAdmin']
            organization_id:
                A string denoting the id of the organization to which the user
                is added.
            backend_instance_id:
                A string denoting the backend instance id.
            language:
                A string denoting the language that is set for the created
                user, defaulting to 'en-US'.
            **kwargs:
                Keyword arguments passed to requests functions.

        Returns:
            The requests response of the lana api call.
        """
        if role not in ['Viewer', 'Analyst', 'RAnalyst', 'UserAdmin',
                        'SuperAdmin']:
            raise Exception('The role has to be one of "Viewer", "Analyst", '
                            + '"RAnalyst", "UserAdmin" or "SuperAdmin".')

        request_data = {'email': email,
                        'role': role,
                        'organizationId': organization_id,
                        'acceptedTerms': False,
                        'ApiKeyStatus': 'Active',
                        'backendInstanceId': backend_instance_id,
                        'preferences': {
                                'language': language
                                }
                        }

        return self.post('/api/users', json = request_data, **kwargs)

    def list_organizations(self, **kwargs) -> list:
        """List all organizations that are allowed to be viewed.

        Args:
            **kwargs:
                Keyword arguments passed to requests functions.

        Returns:
            A list of organizations.
        """

        return self.get('/api/organizations').json()

    def update_user_role(self, user_id: str, role: str,
                         **kwargs) -> Response:
        """Updates the role of an existing user.

        Args:
            user_id:
                A string denoting the user id of the requested user.
            role:
                A string denoting the role of the user. Has to be one
                of ['Viewer', 'Analyst', 'RAnalyst', 'UserAdmin', 'SuperAdmin']
            **kwargs:
                Keyword arguments passed to requests functions.

        Returns:
            The requests response of the lana api call.
        """
        if role not in ['Viewer', 'Analyst', 'RAnalyst', 'UserAdmin',
                        'SuperAdmin']:
            raise Exception('The role has to be one of "Viewer", "Analyst", '
                            + '"RAnalyst", "UserAdmin" or "SuperAdmin".')

        request_data = {'role': role}

        return self.patch('/api/users/' + user_id, json = request_data,
                          **kwargs)

    def update_user_organization(self, user_id: str, organization_id: str,
                                 **kwargs) -> Response:
        """Updates the role of an existing user.

        Args:
            user_id:
                A string denoting the user id of the requested user.
            organization_id:
                A string denoting the id of the organization to which the user
                is added.
            **kwargs:
                Keyword arguments passed to requests functions.

        Returns:
            The requests response of the lana api call.
        """
        request_data = {'organization_id': organization_id}

        return self.patch('/api/users/' + user_id, json = request_data,
                          **kwargs)

    def get_user_information_by_id(self, user_id: str, **kwargs) -> dict:
        """Lists information about a given user.

        Args:
            user_id:
                A string denoting the user id of the requested user.
            **kwargs:
                Keyword arguments passed to requests functions.

        Returns:
            A dictionary containing the user information.
        """
        return self.get('/api/users/' + user_id, **kwargs).json()

    def get_all_users(self, **kwargs) -> list:
        """Get a list with the information about all accessible users.

        Args:
            **kwargs:
                Keyword arguments passed to requests functions.

        Returns:
            A list containing the information about all the users.
        """
        return self.get('/api/users/', **kwargs).json()

    def delete_user(self, user_id: str, **kwargs) -> Response:
        """Deletes a given user from the system.

        Args:
            user_id:
                A string denoting the user id of the requested user.
            **kwargs:
                Keyword arguments passed to requests functions.

        Returns:
            The requests response of the lana api call.
        """
        return self.delete('/api/users/' + user_id, **kwargs)
