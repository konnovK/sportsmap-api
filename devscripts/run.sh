#!/bin/bash

DEV_DB_URL=postgresql+asyncpg://user123:123@localhost:5432/dev_sportsmap_api_db
PYTHON_ENV=venv
PYTHON_EXEC=python3
PYTHON_BIN=$PYTHON_ENV/bin

API_DB_URL=$DEV_DB_URL \
	$PYTHON_BIN/python main.py