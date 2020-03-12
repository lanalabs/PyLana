from dataclasses import dataclass


@dataclass
class User:
    user_id: str
    organization_id: str
    api_key: str
    role: str
