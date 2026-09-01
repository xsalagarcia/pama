from typing import Sequence

from pama.models.account import Account, AccountUpdate
from pama.data import account as data

async def create_account(account: Account) -> Account:
    return await data.create_account(account=account)

async def update_account(account_update: AccountUpdate) -> Account:
    return await data.update_account(account_update=account_update)

async def remove_account(account_id: int):
    await data.remove_account(account_id=account_id)

async def search_account(name: str | None = None, comments: str | None = None,
                         url: str | None = None, limit: int | None = None, offset: int | None = None) -> Sequence[Account]:
    return await search_account(name=name, comments=comments, url=url, limit=limit, offset=offset)

