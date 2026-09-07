import asyncio
from typing import Sequence

from pama.cryptotools import fernet_enc_dec
from pama.exceptions.service import ServiceError
from pama.models.account import Account, AccountUpdate
from pama.data import account as data

enc_dec: None | fernet_enc_dec.FernetEncDecrypt = None

async def create_account(account: Account) -> Account:
    if enc_dec is not None:
        account.passw = enc_dec.encrypt(account.passw)
    else:
        raise ServiceError(msg="Enc / Dec is not set.")
    await data.create_account(account=account)
    return account

async def update_account(account_update: AccountUpdate) -> Account:
    if account_update.passw is not None:
        if enc_dec is None:
            raise ServiceError(msg="Enc / Dec is not set.")
        account_update.passw = enc_dec.encrypt(account_update.passw)
    return await data.update_account(account_update=account_update)

async def remove_account(account_id: int) -> int:
    return await data.remove_account(account_id=account_id)

async def search_account(name: str | None = None, comments: str | None = None,
                         url: str | None = None, limit: int | None = None, offset: int | None = None) -> Sequence[Account]:
    return await data.search_account(name=name, comments=comments, url=url, limit=limit, offset=offset)

def set_encoder(key: bytes, salt: bytes):
    global enc_dec
    enc_dec = fernet_enc_dec.FernetEncDecrypt(key=key, salt=salt)

def decode_pw(encoded: bytes) -> str:
    if enc_dec is not None:
        return enc_dec.decrypt(encoded).decode("utf-8")
    else:
        raise ServiceError(msg="Enc / Dec is not set.")

async def test_async(error: bool):
    if error:
        raise ServiceError(msg="Error raised.")
    await asyncio.sleep(1)
    print("tested")