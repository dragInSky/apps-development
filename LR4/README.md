# LR4 — тестирование бэкенда

Эта лабораторная работает поверх проекта из `LR3`. В `LR4` лежат только конфиги и тесты, сам код приложения остаётся в `LR3`.

## Подготовка
```bash
cd LR4
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Как запустить приложение из LR3
```bash
cd ..
export PYTHONPATH=$(pwd)
uvicorn --app-dir . LR3.app.main:app --reload --port 8000
```

## Как прогнать тесты
```bash
cd LR4
source venv/bin/activate
PYTHONPATH=$(pwd)/.. pytest
PYTHONPATH=$(pwd)/.. pytest tests/test_repositories/ tests/test_services/
PYTHONPATH=$(pwd)/.. pytest tests/test_routes/
PYTHONPATH=$(pwd)/.. pytest --cov=LR3 --cov-report=html
PYTHONPATH=$(pwd)/.. pytest -n auto
```
