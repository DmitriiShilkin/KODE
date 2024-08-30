#!/usr/bin/env bash
# -*- coding: utf-8 -*-
export ENVIRONMENT=tests
export PYTHONDONTWRITEBYTECODE=1
main_env_tests=src/.env.tests

docker compose -f docker/docker-compose-tests.yml up -d --build
docker compose -f docker/docker-compose-tests.yml run --rm kode-core-tests pytest -x
docker compose -f docker/docker-compose-tests.yml down
