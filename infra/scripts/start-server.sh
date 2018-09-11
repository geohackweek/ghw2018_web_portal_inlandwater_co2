#!/usr/bin/env bash

set -e

source activate backend;
infra/scripts/wait-for-postgres.sh python src/backend/server/manage.py migrate;
python src/backend/server/manage.py runserver 0.0.0.0:8000;