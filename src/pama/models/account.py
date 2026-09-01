from datetime import datetime

from sqlmodel import SQLModel, Field, DateTime
from sqlalchemy import Column, text, TIMESTAMP, func

from pama.settings.settings import config


class Account(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(max_length=127, unique=True)
    comments: str = Field(max_length=254)
    url: str = Field()
    passw: bytes = Field()
    last_updated: datetime | None = Field(
        sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    )


class AccountUpdate(SQLModel):
    id: int
    name: str | None = Field(max_length=127, default=None)
    comments: str | None = Field(max_length=254, default=None)
    url: str | None = Field(default=None)
    passw: bytes | None = Field(default=None)