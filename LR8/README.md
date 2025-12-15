# LR8 — Планировщик (TaskIQ) + отчёты по заказам

## Миграция (SQL)
Файл: `LR8/migrations/001_create_order_report_view.sql`.

В проекте view также создаётся на старте приложения (см. `LR3/app/dependencies.py`), чтобы можно было работать без ручного применения SQL.

## Как запустить
Поднять сервисы (Postgres + RabbitMQ + Redis + API + workers):
```bash
cd ..
docker compose -f LR5/docker-compose.yml up -d --build
```

Проверить API:
```bash
curl -f http://localhost:8000/users
```

Проверить логи:
```bash
docker logs -n 200 lr8_taskiq_scheduler
docker logs -n 200 lr8_taskiq_worker
```

UI RabbitMQ: `http://localhost:15672` (логин/пароль: `guest`/`guest`).

## Получить отчёт из API
```bash
curl -s -X POST http://localhost:8000/report \
  -H 'content-type: application/json' \
  -d '{"report_at":"2025-12-14"}'
```
