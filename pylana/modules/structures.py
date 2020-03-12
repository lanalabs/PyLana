from dataclasses import dataclass


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
class Log:
    """
    connection about a log's name and its id
    """
    name: str
    log_id: str
