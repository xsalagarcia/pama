from typing import Sequence

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import delete, select, col

from pama.data.engine import with_session
from pama.exceptions.database import DatabaseError
from pama.models.account import Account, AccountUpdate


@with_session(final_autocommit=True)
async def create_account(session: AsyncSession, account: Account):
    session.add(account)

@with_session()
async def update_account(session: AsyncSession, account_update: AccountUpdate) -> Account:
    account_db: Account | None = await session.get(Account, account_update.id)
    if not account_db:
        raise DatabaseError(msg="Account not found")

    account_db.sqlmodel_update(account_update.model_dump(exclude_unset=True))
    session.add(account_db)
    await session.commit()
    await session.refresh(account_db)
    return account_db

@with_session(final_autocommit=True)
async def remove_account(session: AsyncSession, account_id: int) -> int:
    return (await session.exec(delete(Account).where(col(Account.id) == account_id))).rowcount

@with_session()
async def search_account(session: AsyncSession, name: str | None = None, comments: str | None = None,
                         url: str | None = None, limit: int | None = None, offset: int | None = None) -> Sequence[Account]:
    stmt = (select(Account).order_by(Account.name))

    if name:
        stmt = stmt.where(col(Account.name).contains(name))
    if comments:
        stmt = stmt.where(col(Account.comments).contains(comments))
    if url:
        stmt = stmt.where(col(Account.url).contains(url))
    if limit:
        stmt = stmt.limit(limit)
    if offset:
        stmt = stmt.offset(offset)

    return (await session.exec(stmt)).fetchall()

