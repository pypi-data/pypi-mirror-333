from dataclasses import dataclass
from functools import cached_property
from threading import local

import aiohttp

from tooi.auth import AuthContext, load_auth_context
from tooi.entities import Account, Status
from tooi.settings import Configuration


_local = local()


@dataclass
class Context:
    auth: AuthContext
    config: Configuration
    _session: aiohttp.ClientSession | None = None

    @cached_property
    def session(self) -> aiohttp.ClientSession:
        return create_client_session(self.auth)


def set_context(context: Context) -> None:
    _local.context = context


def create_context() -> Context:
    config = Configuration()
    auth = load_auth_context()
    return Context(auth, config)


def create_client_session(auth: AuthContext):
    return aiohttp.ClientSession(
        base_url=auth.base_url,
        headers={"Authorization": f"Bearer {auth.access_token}"},
    )


def get_context() -> Context:
    return _local.context


def account_name(acct: str) -> str:
    """
    Mastodon does not include the instance name for local account, this
    functions adds the current instance name to the account name if it's
    missing.
    """
    if "@" in acct:
        return acct

    ctx = get_context()
    return f"{acct}@{ctx.auth.domain}"


def is_mine(status: Status):
    return is_me(status.account)


def is_me(account: Account):
    context = get_context()
    return account_name(account.acct) == context.auth.acct
