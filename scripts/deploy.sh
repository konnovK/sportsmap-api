#!/usr/bin/env sh

echo "${OAUTH}" | docker login --username oauth --password-stdin cr.yandex

docker build --build-arg API_PORT=${API_PORT} --tag=cr.yandex/${REGISTRY_ID}/sportsmap-backend-new:v${VERSION} ../api/

docker push cr.yandex/${REGISTRY_ID}/sportsmap-backend-new:v${VERSION}