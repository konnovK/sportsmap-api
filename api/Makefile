DEV_DB_URL=postgresql+asyncpg://user123:123@localhost:5432/dev_sportsmap_api_db
TEST_DB_URL=postgresql+asyncpg://user123:123@localhost:5433/test_sportsmap_api_db

PYTHON_ENV=../venv

PYTHON_EXEC=python3.10
PYTHON_BIN=$(PYTHON_ENV)/bin
ifeq ($(OS), Windows_NT)
	PYTHON_BIN=$(PYTHON_ENV)/Scripts
	PYTHON_EXEC=python
endif

devenv:
	rm -rf $(PYTHON_ENV)
	$(PYTHON_EXEC) -m venv $(PYTHON_ENV)
	$(PYTHON_BIN)/pip install --upgrade pip
	$(PYTHON_BIN)/pip install -r requirements.txt

postgres:
	docker stop dev_sportsmap_api_db || true
	docker stop test_sportsmap_api_db || true
	docker run --rm --detach --name=dev_sportsmap_api_db \
		--env POSTGRES_USER=user123 \
		--env POSTGRES_PASSWORD=123 \
		--env POSTGRES_DB=dev_sportsmap_api_db \
		--publish 5432:5432 postgres
	docker run --rm --detach --name=test_sportsmap_api_db \
		--env POSTGRES_USER=user123 \
		--env POSTGRES_PASSWORD=123 \
		--env POSTGRES_DB=test_sportsmap_api_db \
		--publish 5433:5432 postgres
	@sleep 2

migrate:
	$(PYTHON_BIN)/python -m db --db-url $(DEV_DB_URL) upgrade head

make_migration:
	$(PYTHON_BIN)/python -m db --db-url $(DEV_DB_URL) revision --message="some migration" --autogenerate

lint:
	$(PYTHON_BIN)/pylama

test: lint
	API_DB_URL=$(TEST_DB_URL) \
	$(PYTHON_BIN)/pytest -W ignore::DeprecationWarning --cov-report term-missing --cov --durations=0

run:
	API_DB_URL=$(TEST_DB_URL) \
	$(PYTHON_BIN)/python main.py
