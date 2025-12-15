# LR5 — форматирование, линтинг и Docker

Лабораторная работа собрана поверх проекта из `LR3` и тестов из `LR4`. В корне репозитория лежат конфиги линтеров/форматеров, а в `LR5` — зависимости и Docker-артефакты. 
Все команды ниже выполняются из корня репозитория.

## Подготовка
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
source LR5/venv/bin/activate
```

## Линтинг и форматирование
- Установка и запуск хуков:
  ```bash
  cd ..
  source LR5/venv/bin/activate
  pre-commit install
  pre-commit run --all-files
  ```
- Ручные команды (используют те же конфиги):
  ```bash
  cd ..
  source LR5/venv/bin/activate
  black --config pyproject.toml LR3 LR4/tests LR5
  isort --settings-path pyproject.toml LR3 LR4/tests LR5
  pylint --rcfile .pylintrc LR3
  ```

## Тесты (из ЛР4)
```bash
cd ..
source LR5/venv/bin/activate
export PYTHONPATH=$(pwd)
pytest LR4/tests --verbose --color=yes
```

## Docker
При появлении миграций Alembic можно заменить блок инициализации в `entrypoint.sh` на `alembic upgrade head`.

Запуск через Compose:
```bash
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up
```
