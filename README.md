# Deribit Price API

Сервис раз в минуту получает индексные цены `btc_usd` и `eth_usd` из Deribit, сохраняет их в PostgreSQL и предоставляет HTTP API.

## Развёртывание

Для запуска нужен Docker Desktop с запущенным Linux-контейнерным движком.

В корне проекта создайте `.env`:

```env
DATABASE_URL=postgresql+asyncpg://deribit:deribit@postgres:5432/deribit
CELERY_BROKER_URL=redis://redis:6379/0
DERIBIT_API_URL=https://www.deribit.com/api/v2/public/get_index_price
```

Запустите приложение:

```bash
docker compose up --build
```

Compose запускает PostgreSQL и Redis, применяет Alembic-миграцию, затем запускает API, Celery worker, Celery Beat и Flower.

Проверить результат можно по адресам:

- API: `http://localhost:8000/docs`
- Flower: `http://localhost:5555`

Остановить сервисы:

```bash
docker compose down
```

Данные PostgreSQL сохраняются в named volume `postgres_data`.

## API

Во всех запросах обязателен query-параметр `ticker` со значением `btc` или `eth`.

| Метод | Назначение |
| --- | --- |
| `GET /prices?ticker=btc` | Все сохранённые цены тикера |
| `GET /prices/latest?ticker=btc` | Последняя цена тикера |
| `GET /prices/by-date?ticker=btc&date=2024-01-01` | Цены тикера за UTC-день |

Если данных по тикеру нет, `GET /prices/latest` возвращает `404`; остальные методы возвращают пустой список.

## Тесты

```bash
uv sync --all-groups
uv run pytest
```

Тесты не требуют запущенных PostgreSQL, Redis или Docker.

## Design decisions

- Цена хранится как `float`: сервис не выполняет денежные расчёты.
- Время хранится как UNIX timestamp в UTC; фильтр даты также интерпретируется в UTC.
- Клиент Deribit использует асинхронный `aiohttp`; цены BTC и ETH запрашиваются параллельно в одном цикле сбора.
- FastAPI создаёт SQLAlchemy engine и session factory на весь lifespan приложения. Worker создаёт временный engine на один запуск задачи, поскольку `asyncio.run` создаёт отдельный event loop.
- Alembic-миграция создаёт схему до старта API и worker; Celery-задача не выполняет DDL.
- Celery повторяет временные сетевые и SQL-ошибки до пяти раз с экспоненциальной задержкой и jitter.
