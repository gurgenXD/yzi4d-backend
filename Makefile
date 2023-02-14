PYTHONPATH = export PYTHONPATH=./
POETRY_RUN = poetry run


.PHONY: migrations-make
migration-make: ## Создать миграцию базы данных.
	$(POETRY_RUN) python manage.py migrations make "Migration message."

.PHONY: migrations-up
migrations-up: ## Накатить миграции.
	$(POETRY_RUN) python manage.py migrations up

.PHONY: migrations-down
migrations-down: ## Откатить последнюю миграцию.
	$(POETRY_RUN) python manage.py migrations down

.PHONY: start-api
start-api: ## Запусть API.
	$(POETRY_RUN) python manage.py start api


.PHONY: lint
lint: ## Проверить код.
	$(POETRY_RUN) black --check .
	$(POETRY_RUN) ruff check .

.PHONY: test
test: ## Запустить тесты.
	$(PYTHONPATH) && $(POETRY_RUN) pytest tests --cov=./ --cov-report html

.PHONY: format
format: ## Отформатировать все файлы.
	$(POETRY_RUN) isort .
	$(POETRY_RUN) black .

.PHONY: docker-up
docker-up: ## Запустить инфраструктуру для локальной разрабоки.
	docker-compose -f ./cicd/docker-compose.local.yml up -d
