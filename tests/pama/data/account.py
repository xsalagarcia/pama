import asyncio
import unittest

from sqlalchemy import inspect

from pama.data.engine import restart_db
from pama.models.account import Account, AccountUpdate
from pama.data import account as data


class TestAccount(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await restart_db()
    async def test_create_account(self):
        account = Account(name="test name", comments="test comments", url="test url", passw=b"some test bytes")
        self.assertTrue(inspect(account).transient)
        self.assertFalse(inspect(account).detached)
        await data.create_account(account=account)
        self.assertFalse(inspect(account).transient)
        self.assertTrue(inspect(account).detached)
        return account

    async def test_update_account(self):
        account = await self.test_create_account()

        await asyncio.sleep(1)  # 1s precision for last_updated
        account_update = AccountUpdate(id=account.id, name="changed name")
        updated_account = await data.update_account(account_update=account_update)
        self.assertEqual(updated_account.name, "changed name")
        self.assertTrue(updated_account.last_updated > account.last_updated)
        self.assertFalse(inspect(updated_account).transient)
        self.assertTrue(inspect(updated_account).detached)

    async def test_remove_account(self):
        account = await self.test_create_account()

        self.assertEqual(await data.remove_account(account_id=account.id), 1)
        self.assertEqual(await data.remove_account(account_id=account.id), 0)

    async def test_search_account(self):
        [await data.create_account(account=Account(name=f"account {i}", comments=f"comment {i}",
                                                   url=f"url {i}", passw=b"passw")) for i in range(1, 21)]

        self.assertEqual(len(await data.search_account()), 20)
        self.assertEqual(len(await data.search_account(name="1")), 11)
        self.assertEqual(len(await data.search_account(comments="comment 2")), 2)
        self.assertEqual(len(await data.search_account(limit=10)), 10)
        self.assertEqual((await data.search_account(limit=10))[0].name, "account 1")
        self.assertEqual((await data.search_account(limit=10, offset=2))[0].name, "account 11")  # Alphabetically name 1, name 11, name 12...






