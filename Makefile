include .env

PROJECT_NAME=sportsmap_api
VERSION=0

PYTHON_ENV=venv
PYTHON_BIN=$(PYTHON_ENV)/bin

ifeq ($(OS), Windows_NT)
	PYTHON_BIN=$(PYTHON_ENV)/Scripts
endif

all:
	@echo "make devenv		- Создать окружение разработки"
	@echo "make lint		- Проверить код линтером pylama"
	@echo "make test		- Запустить тесты"
	@exit 0

devenv:
	rm -rf $(PYTHON_ENV)
	python -m venv $(PYTHON_ENV)
	$(PYTHON_BIN)/pip install --upgrade pip
	$(PYTHON_BIN)/pip install -r requirements.txt

lint:
	$(PYTHON_BIN)/pylama

test: lint
	API_PORT=$(API_PORT) \
	API_DB_USER=$(API_DB_USER) \
	API_DB_PASSWORD=$(API_DB_PASSWORD) \
	API_DB_HOST=$(API_DB_HOST) \
	API_DB_PORT=$(API_DB_PORT) \
	API_DB_NAME=$(API_DB_NAME) \
	$(PYTHON_BIN)/pytest
