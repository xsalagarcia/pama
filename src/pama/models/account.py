from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, text, TIMESTAMP


class Account(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(max_length=127, unique=True)
    comments: str = Field(max_length=254)
    url: str = Field()
    passw: bytes = Field()
    last_updated: datetime | None = Field(sa_column=Column(TIMESTAMP(timezone=True),
                                                           server_default=text("NOW()") # server_default text: NOW() for postgresql, CURRENT_TIMESTAMP for sqlite
                                                           ))
