"""
data classes
"""

from dataclasses import dataclass, field
from typing import List


@dataclass(eq=True, frozen=True)
class User:
    """
    information about a user required for accessing the API
    """
    user_id: str
    organization_id: str
    api_key: str
    role: str


@dataclass(eq=True, frozen=True)
class SharedInformation:
    """
    sharing information of a resource
    """
    user_ids: List[str] = field(default_factory=list)
    project_ids: List[str] = field(default_factory=list)
    organization_ids: List[str] = field(default_factory=list)


@dataclass(eq=True, frozen=True)
class Resource:
    """
    a generic resource depicting logs, models, shiny dashboards etc.
    """
    name: str
    id: str


class Log(Resource):
    pass


class ShinyDashboard(Resource):
    owner: str
    shared_information: SharedInformation = field(default_factory=SharedInformation)
