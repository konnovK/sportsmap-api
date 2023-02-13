#!/bin/bash

PYTHON_ENV=venv
PYTHON_EXEC=python3
PYTHON_BIN=$PYTHON_ENV/bin

rm -rf $PYTHON_ENV
$PYTHON_EXEC -m venv $PYTHON_ENV
$PYTHON_BIN/pip install --upgrade pip
$PYTHON_BIN/pip install -r ../requirements.txt