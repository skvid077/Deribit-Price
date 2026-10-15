from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession


def create_session_mock() -> MagicMock:
    session = MagicMock(spec=AsyncSession)
    session.scalar = AsyncMock()
    session.scalars = AsyncMock()
    session.scalars.return_value = MagicMock()
    session.commit = AsyncMock()
    return session


def create_aiohttp_response_mock(index_price: float) -> MagicMock:
    response = MagicMock()
    response.json = AsyncMock(return_value={"result": {"index_price": index_price}})
    return response


def create_aiohttp_session_mock(response: MagicMock) -> tuple[MagicMock, MagicMock]:
    request_session = MagicMock()
    request_session.get.return_value.__aenter__.return_value = response
    client_session = MagicMock()
    client_session.__aenter__.return_value = request_session
    return client_session, request_session
