# LR3 - REST API с Dependency Injection

Простое API для работы с пользователями. Используется Litestar, SQLAlchemy и PostgreSQL.

## Установка

```bash
cd LR3
python -m venv venv
source venv/bin/activate  # на Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## База данных

Нужен PostgreSQL. По умолчанию подключается к `postgres:postgres@localhost/my_postgres_db`.

Если базы нет, создай:
```bash
createdb -U postgres my_postgres_db
```

Таблицы создаются автоматически при первом запуске.

## Запуск

**Важно:** запускай из папки `apps-development`, не из `LR3`!

```bash
cd /path/to/apps-development
source LR3/venv/bin/activate
uvicorn LR3.app.main:app --reload --port 8000
```

Или без активации venv:
```bash
cd /path/to/apps-development
LR3/venv/bin/python -m uvicorn LR3.app.main:app --reload --port 8000
```

Сервер будет на `http://127.0.0.1:8000`

## API

Создать пользователя:
```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","full_name":"John Doe"}'
```

Получить всех:
```bash
curl http://127.0.0.1:8000/users
```

Получить по ID:
```bash
curl http://127.0.0.1:8000/users/1
```

Обновить:
```bash
curl -X PUT "http://127.0.0.1:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Jane Doe"}'
```

Удалить:
```bash
curl -X DELETE http://127.0.0.1:8000/users/1
```

## Проблемы

**"ModuleNotFoundError: No module named 'LR3'"** - запускай из `apps-development`, не из `LR3`

**"Address already in use"** - порт занят, используй другой:
```bash
uvicorn LR3.app.main:app --reload --port 8001
```

**Не подключается к БД** - проверь что PostgreSQL запущен и база существует
