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

PYTHON_ENV=venv

PYTHON_EXEC=python3.10
PYTHON_BIN=$(PYTHON_ENV)/bin
ifeq ($(OS), Windows_NT)
	PYTHON_BIN=$(PYTHON_ENV)/Scripts
	PYTHON_EXEC=python
endif

all:
	@echo "make devenv      - Создать окружение разработки"
	@echo "make postgres    - Создать Docker контейнеры с базами данных для тестов и разработки"
	@echo "make migrate     - Накатить миграции на базы данных для тестов и разработки"
	@echo "make lint        - Проверить код линтером pylama"
	@echo "make test        - Запустить тесты (Нужен Docker)"
	@echo "make run         - Запустить API (Нужен Docker)"
	@exit 0

devenv:
	rm -rf $(PYTHON_ENV)
	$(PYTHON_EXEC) -m venv $(PYTHON_ENV)
	$(PYTHON_BIN)/pip install --upgrade pip
	$(PYTHON_BIN)/pip install -r requirements.txt

postgres:
	docker stop $(API_DEV_DB_NAME) || true
	docker stop $(API_TEST_DB_NAME) || true

	docker stop $(PROJECT_NAME) || true

	docker network rm $(PROJECT_NAME) || true
	docker network create $(PROJECT_NAME)

	docker run --rm --detach --name=$(API_DEV_DB_NAME) \
		--env POSTGRES_USER=$(API_DEV_DB_USER) \
		--env POSTGRES_PASSWORD=$(API_DEV_DB_PASSWORD) \
		--env POSTGRES_DB=$(API_DEV_DB_NAME) \
		--network $(PROJECT_NAME) \
		--publish $(API_DEV_DB_PORT):5432 postgres
	docker run --rm --detach --name=$(API_TEST_DB_NAME) \
		--env POSTGRES_USER=$(API_TEST_DB_USER) \
		--env POSTGRES_PASSWORD=$(API_TEST_DB_PASSWORD) \
		--env POSTGRES_DB=$(API_TEST_DB_NAME) \
		--network $(PROJECT_NAME) \
		--publish $(API_TEST_DB_PORT):5432 postgres
	@sleep 2

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

make_migration:
	$(PYTHON_BIN)/$(PYTHON_EXEC) -m db --db-user $(API_DEV_DB_USER) \
 		--db-password $(API_DEV_DB_PASSWORD) \
 		--db-host $(API_DEV_DB_HOST) \
 		--db-port $(API_DEV_DB_PORT) \
 		--db-name $(API_DEV_DB_NAME) revision --message="some migration" --autogenerate

lint:
	$(PYTHON_BIN)/pylama

test: lint
	API_PORT=$(API_PORT) \
	API_DB_USER=$(API_TEST_DB_USER) \
	API_DB_PASSWORD=$(API_TEST_DB_PASSWORD) \
	API_DB_HOST=$(API_TEST_DB_HOST) \
	API_DB_PORT=$(API_TEST_DB_PORT) \
	API_DB_NAME=$(API_TEST_DB_NAME) \
	$(PYTHON_BIN)/pytest -W ignore::DeprecationWarning --cov-report term-missing --cov

run:
	API_PORT=$(API_PORT) \
	API_DB_USER=$(API_DEV_DB_USER) \
	API_DB_PASSWORD=$(API_DEV_DB_PASSWORD) \
	API_DB_HOST=$(API_DEV_DB_HOST) \
	API_DB_PORT=$(API_DEV_DB_PORT) \
	API_DB_NAME=$(API_DEV_DB_NAME) \
	$(PYTHON_BIN)/$(PYTHON_EXEC) main.py

build:
	docker build \
		--build-arg API_PORT=$(API_PORT) \
		--build-arg API_DB_USER=$(API_DEV_DB_USER) \
		--build-arg API_DB_PASSWORD=$(API_DEV_DB_PASSWORD) \
		--build-arg API_DB_HOST=$(API_DEV_DB_NAME) \
		--build-arg API_DB_PORT=$(API_DEV_DB_PORT) \
		--build-arg API_DB_NAME=$(API_DEV_DB_NAME) \
		--network $(PROJECT_NAME) \
		--tag=$(PROJECT_NAME):$(VERSION) .

docker:
	docker stop $(PROJECT_NAME) || true
	docker run --rm --detach --name $(PROJECT_NAME) \
	--env API_DB_USER=$(API_DEV_DB_USER) \
	--env API_DB_PASSWORD=$(API_DEV_DB_PASSWORD) \
	--env API_DB_HOST=$(API_DEV_DB_NAME) \
	--env API_DB_PORT=$(API_DEV_DB_PORT) \
	--env API_DB_NAME=$(API_DEV_DB_NAME) \
	--network $(PROJECT_NAME) \
	--publish $(API_PORT):$(API_PORT) $(PROJECT_NAME):$(VERSION)

# Для прода

include ./deploy/.env

migrate_prod:
	$(PYTHON_BIN)/$(PYTHON_EXEC) -m db --db-user $(DB_USER) \
 		--db-password $(DB_PASSWORD) \
 		--db-host $(DB_HOST) \
 		--db-port $(DB_PORT) \
 		--db-name $(DB_NAME) upgrade head

deploy:
	REGISTRY_ID=$(REGISTRY_ID) \
	TOKEN=$(TOKEN) \
	VERSION=$(VERSION) \
	API_PORT=$(API_PORT) \
	./deploy.sh