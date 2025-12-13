# LR3 — REST API с DI

Минимальное API на Litestar, SQLAlchemy и PostgreSQL для CRUD над пользователями.

## Подготовка

```bash
cd LR3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

## База данных

Запусти PostgreSQL в Docker (рекомендуется):

```bash
docker-compose up -d
```

Параметры подключения: `postgres/postgres@localhost:5432/my_postgres_db`.

Для локального PostgreSQL:

```bash
PGPASSWORD=postgres createdb -h localhost -U postgres my_postgres_db
export DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost/my_postgres_db
```

## Запуск приложения

```bash
cd LR3
export PYTHONPATH=$(pwd)/..
../LR3/venv/bin/uvicorn --app-dir .. LR3.app.main:app --reload --port 8000
```

## Примеры запросов

```bash
BASE=http://127.0.0.1:8000
EMAIL="user$(date +%s)@example.com"

ID=$(
  curl -s -X POST "$BASE/users" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$EMAIL\",\"full_name\":\"John Doe\"}" \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])"
)

curl "$BASE/users"
curl "$BASE/users/$ID"

curl -X PUT "$BASE/users/$ID" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Jane Doe"}'

curl -X DELETE "$BASE/users/$ID"
```
