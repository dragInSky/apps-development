# LR6 — RabbitMQ (FastStream) + Litestar

## Как запустить
Поднять сервисы:
```bash
cd ..
docker compose -f LR5/docker-compose.yml up -d --build
```

Подождать, пока API поднимется на `http://localhost:8000` (если команда падает — просто повторить через несколько секунд):
```bash
cd ..
curl -f http://localhost:8000/users
```

Отправить тестовые данные (создаст 5 продукций и 3 заказа):
```bash
cd ..
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r LR3/requirements.txt
PYTHONPATH=$(pwd) .venv/bin/python -m LR6.producer
```

Проверить результат:
```bash
cd ..
curl http://localhost:8000/products
curl http://localhost:8000/orders
docker logs -n 200 lr6_worker
```

UI RabbitMQ: `http://localhost:15672` (логин - guest, пароль - guest).
