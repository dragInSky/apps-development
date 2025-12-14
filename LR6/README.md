# LR6 — RabbitMQ (FastStream) + Litestar

Цель: добавить брокер сообщений RabbitMQ и обработку очередей `product` и `order` в проект из ЛР5 (Litestar + Postgres).

## Что добавлено
- RabbitMQ (`rabbitmq:3-management`) + UI: `http://localhost:15672` (логин/пароль `guest/guest`)
- Worker на `faststream[rabbit]`, который:
  - принимает продукцию (`product`: создать/обновить/пометить как `out_of_stock`)
  - принимает заказы (`order`: создать/обновить статус)
  - отклоняет заказы, если товара нет / не хватает на складе (см. логи `worker`)
- Получение списка/конкретной продукции и заказов — через Litestar API:
  - `GET /products`, `GET /products/{id}`
  - `GET /orders`, `GET /orders/{id}`

## Запуск через Docker Compose (ЛР5)
Из корня репозитория:
```bash
docker compose -f LR5/docker-compose.yml up --build
```

## Проверка очередей
Worker слушает очереди:
- `product`
- `order`

## Скрипт-продюсер (5 продукций + 3 заказа)
С хоста (локально), при запущенном compose:
```bash
python -m LR6.producer
```

По умолчанию скрипт использует:
- API: `http://localhost:8000` (можно переопределить `API_BASE_URL`)
- RabbitMQ: `localhost:5672`, vhost `local` (можно переопределить `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_VHOST`)

## Формат сообщений
Очередь `product`:
- создать:
  ```json
  {"action":"create","product":{"name":"Laptop","price":1200.0,"stock_quantity":5,"description":"..." }}
  ```
- обновить:
  ```json
  {"action":"update","product_id":1,"product":{"price":999.0,"stock_quantity":10}}
  ```
- пометить как закончившийся:
  ```json
  {"action":"out_of_stock","product_id":1}
  ```

Очередь `order`:
- создать:
  ```json
  {"action":"create","order":{"user_id":1,"items":[{"product_id":1,"quantity":2}]}}
  ```
- обновить статус:
  ```json
  {"action":"update_status","order_id":1,"status":"paid"}
  ```

