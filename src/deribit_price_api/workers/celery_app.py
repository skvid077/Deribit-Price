from celery import Celery

from deribit_price_api.core.settings import get_broker_settings

celery_app = Celery(
    "deribit_prices",
    broker=get_broker_settings().celery_broker_url,
    include=["deribit_price_api.workers.tasks"],
)
celery_app.conf.update(
    beat_schedule={
        "fetch-index-prices-every-minute": {
            "task": "deribit_price_api.workers.tasks.fetch_index_prices",
            "schedule": 60.0,
        }
    },
    timezone="UTC",
)
