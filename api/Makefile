PROJECT_NAME=sportsmap_api
VERSION=1

API_PORT=8080

API_DEV_DB_USER=user123
API_DEV_DB_PASSWORD=123
API_DEV_DB_HOST=localhost
API_DEV_DB_PORT=5432
API_DEV_DB_NAME=dev_sportsmap_api_db

API_TEST_DB_USER=user123
API_TEST_DB_PASSWORD=123
API_TEST_DB_HOST=localhost
API_TEST_DB_PORT=5433
API_TEST_DB_NAME=test_sportsmap_api_db

PYTHON_ENV=../venv

PYTHON_EXEC=python3
PYTHON_BIN=$(PYTHON_ENV)/bin
ifeq ($(OS), Windows_NT)
	PYTHON_BIN=$(PYTHON_ENV)/Scripts
	PYTHON_EXEC=python
endif

migrate:
	$(PYTHON_BIN)/$(PYTHON_EXEC) -m db --db-user $(API_DEV_DB_USER) \
 		--db-password $(API_DEV_DB_PASSWORD) \
 		--db-host $(API_DEV_DB_HOST) \
 		--db-port $(API_DEV_DB_PORT) \
 		--db-name $(API_DEV_DB_NAME) upgrade head
	$(PYTHON_BIN)/$(PYTHON_EXEC) -m db --db-user $(API_TEST_DB_USER) \
		--db-password $(API_TEST_DB_PASSWORD) \
		--db-host $(API_TEST_DB_HOST) \
		--db-port $(API_TEST_DB_PORT) \
		--db-name $(API_TEST_DB_NAME) upgrade head