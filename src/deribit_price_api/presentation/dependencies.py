import collections.abc as cabc
import typing as tp

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from deribit_price_api.infrastructure.database import Database


async def get_session(request: Request) -> cabc.AsyncGenerator[AsyncSession]:
    database = tp.cast(Database, request.app.state.database)
    async with database.session_scope() as session:
        yield session
