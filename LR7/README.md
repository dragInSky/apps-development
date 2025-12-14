# LR7 — Redis + кэширование в API

## Как запустить
Поднять сервисы:
```bash
cd ..
docker compose -f LR5/docker-compose.yml up -d --build
```

Запустить демо-скрипт:
```bash
cd ..
python3 -m venv .venv
.venv/bin/python -m pip install -r LR3/requirements.txt
PYTHONPATH=$(pwd) .venv/bin/python -m LR7.redis_demo
```

Пример проверки кэша:
```bash
curl -s -X POST http://localhost:8000/users \
  -H 'content-type: application/json' \
  -d '{"email":"u1@example.com","username":"user1","first_name":"Ivan","last_name":"Ivanov"}'
curl -s http://localhost:8000/users/1
docker exec -it redis redis-cli get user:1
```
