#!/bin/bash

docker stop dev_sportsmap_api_db
docker stop test_sportsmap_api_db

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

sleep 2