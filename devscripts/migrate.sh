#!/bin/bash

DEV_DB_URL=postgresql+asyncpg://user123:123@localhost:5432/dev_sportsmap_api_db
PYTHON_ENV=venv
PYTHON_EXEC=python3
PYTHON_BIN=$PYTHON_ENV/bin

$PYTHON_BIN/python -m db --db-url $DEV_DB_URL upgrade head