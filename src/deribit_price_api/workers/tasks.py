import asyncio
import logging
import time as tm

import aiohttp
from sqlalchemy.exc import SQLAlchemyError

from deribit_price_api.application.services.price_collector import PriceCollector
from deribit_price_api.core.settings import get_worker_settings
from deribit_price_api.infrastructure.database import session_scope
from deribit_price_api.infrastructure.repositories.prices import PriceRepository
from deribit_price_api.integrations.deribit import DeribitClient
from deribit_price_api.workers.celery_app import celery_app


@celery_app.task(
    name="deribit_price_api.workers.tasks.fetch_index_prices",
    autoretry_for=(aiohttp.ClientError, TimeoutError, SQLAlchemyError),
    retry_backoff=2,
    retry_backoff_max=300,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def fetch_index_prices() -> None:
    try:
        asyncio.run(_fetch_index_prices_async())
    except (aiohttp.ClientError, TimeoutError, SQLAlchemyError):
        logging.getLogger(__name__).warning("Failed to collect index prices; retrying", exc_info=True)
        raise


async def _fetch_index_prices_async() -> None:
    settings = get_worker_settings()
    async with session_scope(settings.database_url) as session:
        client = DeribitClient(settings.deribit_api_url)
        collector = PriceCollector(client, PriceRepository(session))
        await collector.collect(int(tm.time()))
