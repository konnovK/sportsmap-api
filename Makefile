include .env

PYTHON_ENV=venv

PYTHON_EXEC=python3.10
PYTHON_BIN=$(PYTHON_ENV)/bin
ifeq ($(OS), Windows_NT)
	PYTHON_BIN=$(PYTHON_ENV)/Scripts
	PYTHON_EXEC=python
endif

migrate_prod:
	$(PYTHON_BIN)/$(PYTHON_EXEC) -m db --db-url $(DB_URL) upgrade head

deploy:
	REGISTRY_ID=$(REGISTRY_ID) \
	TOKEN=$(TOKEN) \
	VERSION=$(VERSION) \
	API_PORT=$(API_PORT) \
	./deploy.sh
