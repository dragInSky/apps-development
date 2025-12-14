#!/bin/bash
set -euo pipefail

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
RABBITMQ_HOST="${RABBITMQ_HOST:-}"
RABBITMQ_PORT="${RABBITMQ_PORT:-5672}"

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 0.1
done

if [[ -n "$RABBITMQ_HOST" ]]; then
  while ! nc -z "$RABBITMQ_HOST" "$RABBITMQ_PORT"; do
    sleep 0.1
  done
fi

python - <<'PY'
import asyncio
import os

from LR3.app.dependencies import configure_engine, init_db

db_url = os.getenv("DATABASE_URL")
if db_url:
    configure_engine(db_url)

asyncio.run(init_db())
PY

exec "$@"
