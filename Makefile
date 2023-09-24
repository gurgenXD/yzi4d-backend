PYTHONPATH = export PYTHONPATH=./
POETRY_RUN = poetry run


migrations-make: ## Создать миграцию базы данных.
	$(POETRY_RUN) python -m cli migrations make "Initial commit."

migrations-up: ## Накатить миграции.
	$(POETRY_RUN) python -m cli migrations up

migrations-down: ## Откатить последнюю миграцию.
	$(POETRY_RUN) python -m cli migrations down

start-api: ## Запусть API.
	$(POETRY_RUN) python -m cli start api


lint: ## Проверить код.
	$(POETRY_RUN) black --check .
	$(POETRY_RUN) ruff check .
	$(POETRY_RUN) mypy .

test: ## Запустить тесты.
	$(PYTHONPATH) && $(POETRY_RUN) pytest tests --cov=./ --cov-report html

format: ## Отформатировать все файлы.
	$(POETRY_RUN) black .
	$(POETRY_RUN) ruff check . --fix

docker-up: ## Запустить инфраструктуру для локальной разрабоки.
	docker-compose -f ./cicd/docker-compose.local.yml up -d
