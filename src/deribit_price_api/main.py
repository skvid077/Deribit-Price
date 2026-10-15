from contextlib import asynccontextmanager

from fastapi import FastAPI

from deribit_price_api.core.settings import get_database_settings
from deribit_price_api.infrastructure.database import Database
from deribit_price_api.presentation.api.prices import router as prices_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with Database(get_database_settings().database_url) as database:
        application.state.database = database
        yield


def create_app() -> FastAPI:
    _app = FastAPI(title="Deribit Price API", version="1.0.0", lifespan=lifespan)
    _app.include_router(prices_router)
    return _app


app = create_app()
