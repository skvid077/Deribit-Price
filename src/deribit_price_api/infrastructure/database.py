import collections.abc as cabc
import contextlib

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self, database_url: str) -> None:
        self._engine = create_async_engine(database_url, pool_pre_ping=True)
        self._session_factory = async_sessionmaker(self._engine, expire_on_commit=False)

    async def __aenter__(self) -> "Database":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.dispose()

    @contextlib.asynccontextmanager
    async def session_scope(self) -> cabc.AsyncGenerator[AsyncSession]:
        async with self._session_factory() as session:
            yield session

    async def dispose(self) -> None:
        await self._engine.dispose()


@contextlib.asynccontextmanager
async def session_scope(database_url: str) -> cabc.AsyncGenerator[AsyncSession]:
    database = Database(database_url)
    try:
        async with database.session_scope() as session:
            yield session
    finally:
        await database.dispose()
