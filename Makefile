API_PORT=8080
API_DB_USER=user123
API_DB_PASSWORD=123
API_DB_HOST=localhost
API_DB_PORT=5432
API_DEV_DB_NAME=dev_sportsmap_db
API_TEST_DB_NAME=test_sportsmap_db

PROJECT_NAME=sportsmap_api
VERSION=1

PYTHON_ENV=venv

PYTHON_EXEC=python3.10

PYTHON_BIN=$(PYTHON_ENV)/bin

ifeq ($(OS), Windows_NT)
	PYTHON_BIN=$(PYTHON_ENV)/Scripts
	PYTHON_EXEC=python
endif

all:
	@echo "make devenv      - Создать окружение разработки"
	@echo "make lint        - Проверить код линтером pylama"
	@echo "make test        - Запустить тесты (Нужен Docker)"
	@echo "make run         - Запустить API (Нужен Docker)"
	@exit 0

devenv:
	rm -rf $(PYTHON_ENV)
	$(PYTHON_EXEC) -m venv $(PYTHON_ENV)
	$(PYTHON_BIN)/pip install --upgrade pip
	$(PYTHON_BIN)/pip install -r requirements.txt

postgresdev:
	docker stop sportsmap_db || true
	docker run --rm --detach --name=sportsmap_db \
		--env POSTGRES_USER=$(API_DB_USER) \
		--env POSTGRES_PASSWORD=$(API_DB_PASSWORD) \
		--env POSTGRES_DB=$(API_DEV_DB_NAME) \
		--publish 5432:5432 postgres
	@sleep 2

postgrestest:
	docker stop sportsmap_db || true
	docker run --rm --detach --name=sportsmap_db \
		--env POSTGRES_USER=$(API_DB_USER) \
		--env POSTGRES_PASSWORD=$(API_DB_PASSWORD) \
		--env POSTGRES_DB=$(API_TEST_DB_NAME) \
		--publish 5432:5432 postgres
	@sleep 2

lint:
	$(PYTHON_BIN)/pylama

test: lint postgrestest
	API_PORT=$(API_PORT) \
	API_DB_USER=$(API_DB_USER) \
	API_DB_PASSWORD=$(API_DB_PASSWORD) \
	API_DB_HOST=$(API_DB_HOST) \
	API_DB_PORT=$(API_DB_PORT) \
	API_DB_NAME=$(API_TEST_DB_NAME) \
	$(PYTHON_BIN)/pytest -W ignore::DeprecationWarning

run: postgresdev
	API_PORT=$(API_PORT) \
	API_DB_USER=$(API_DB_USER) \
	API_DB_PASSWORD=$(API_DB_PASSWORD) \
	API_DB_HOST=$(API_DB_HOST) \
	API_DB_PORT=$(API_DB_PORT) \
	API_DB_NAME=$(API_DEV_DB_NAME) \
	$(PYTHON_BIN)/$(PYTHON_EXEC) main.py
