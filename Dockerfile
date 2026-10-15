FROM python:3.15-slim-bookworm

WORKDIR /service
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends --yes build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --root-user-action=ignore uv==0.13.1

COPY alembic.ini ./
COPY pyproject.toml README.md uv.lock ./
COPY migrations ./migrations
COPY src ./src
RUN uv sync --locked --no-dev \
    && uv cache clean \
    && apt-get purge --auto-remove --yes build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system application \
    && useradd --create-home --system --gid application application \
    && chown --recursive application:application /service

USER application
CMD ["uv", "run", "--no-sync", "uvicorn", "deribit_price_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
