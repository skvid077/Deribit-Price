import functools as ft

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DatabaseSettings(EnvironmentSettings):
    database_url: str


class WorkerSettings(EnvironmentSettings):
    database_url: str
    celery_broker_url: str
    deribit_api_url: str


class BrokerSettings(EnvironmentSettings):
    celery_broker_url: str


@ft.lru_cache
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


@ft.lru_cache
def get_worker_settings() -> WorkerSettings:
    return WorkerSettings()


@ft.lru_cache
def get_broker_settings() -> BrokerSettings:
    return BrokerSettings()


