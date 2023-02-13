#!/bin/bash

TEST_DB_URL=postgresql+asyncpg://user123:123@localhost:5433/test_sportsmap_api_db
PYTHON_ENV=venv
PYTHON_EXEC=python3
PYTHON_BIN=$PYTHON_ENV/bin

API_DB_URL=$TEST_DB_URL \
  $PYTHON_BIN/pytest -W ignore::DeprecationWarning --cov-report term-missing --cov --durations=0