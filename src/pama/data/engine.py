import asyncio
from functools import wraps
from typing import Callable, Coroutine, Any

from sqlalchemy.exc import ArgumentError, SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from pama.exceptions.database import DatabaseError
from pama.settings.settings import config
from pama.data.tables import *


engine: AsyncEngine | None = None  # = create_async_engine(url=config.database_url, **config.database_engine_kw)
async_session: async_sessionmaker[AsyncSession | Any] | None = None  # = async_sessionmaker(engine, expire_on_commit=False)


def create_engine(url: str | None = None):

    global engine, async_session
    try:
        engine = create_async_engine(url=config.database_url if url is None else url, **config.database_engine_kw)
        async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    except ArgumentError as e:
        raise DatabaseError(msg=e.args[0])

create_engine()


def with_session(final_autocommit: bool = False):
    """
    Gives session context to the decorated coroutine. For UPDATE, INSERT and DELETE operations
    set final_autocommit=True and ``AsyncSessionTransaction`` context will be created, and a
    commit will be implicitly done and awaited.
    :param final_autocommit:
    :return:
    :raise DatabaseError: If a problem with database occurs.
    """

    def decorator(sessioned_function: Callable[..., Coroutine[Any, Any, Any]]):
        """
        Gives session context to the decorated coroutine.
        The first argument of the decorated coroutine will be ``session: AsyncSession``.
        Catches generic SQLAlchemyError and raises DatabaseError.
        :param sessioned_function: An async function that takes an AsyncSession as its first argument
        """

        @wraps(sessioned_function)
        async def wrapper(*args, **kwargs):
            async with async_session() as session:
                #try:
                    if final_autocommit:
                        async with session.begin():
                            return await sessioned_function(session, *args, **kwargs)
                    else:
                        return await sessioned_function(session, *args, **kwargs)
                #except SQLAlchemyError as e:

                #    raise DatabaseError(msg=str(e))

        return wrapper

    return decorator

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)  # Create database and tables if they doesn't exist.


async def restart_db():
    """
    Delete all and create tables again. For test purpose.
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
