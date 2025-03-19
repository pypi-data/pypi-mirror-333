import json

from dataclasses import dataclass
from os import path
from typing import Any


AUTH_CONTEXT_PATH = path.expanduser("~/.config/toot/config.json")


class NotLoggedInError(Exception):
    ...


@dataclass
class AuthContext:
    acct: str
    domain: str
    base_url: str
    access_token: str


# TODO: uses toot config
def load_auth_context() -> AuthContext:
    actx = _read_auth_context()
    return _parse_auth_context(actx)


def _parse_auth_context(config: dict[str, Any]):
    active_user = config["active_user"]

    if not active_user:
        raise NotLoggedInError()

    user_data = config["users"][active_user]
    instance_data = config["apps"][user_data["instance"]]
    domain = instance_data["instance"]
    base_url = instance_data["base_url"]
    access_token = user_data["access_token"]

    return AuthContext(active_user, domain, base_url, access_token)


def _read_auth_context():
    if path.exists(AUTH_CONTEXT_PATH):
        with open(AUTH_CONTEXT_PATH) as f:
            return json.load(f)

    raise ValueError(f"Authentication config file not found at: {AUTH_CONTEXT_PATH}")
