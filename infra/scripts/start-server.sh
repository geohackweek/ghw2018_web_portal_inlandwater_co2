#!/usr/bin/env bash

set -e

source activate backend;
infra/scripts/wait-for-postgres.sh;
python src/backend/server/manage.py migrate;
python notebooks/load_data_to_postgis.py;
python src/backend/server/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('co2master', 'co2master@example.com', 'co2masterpass')";
python src/backend/server/manage.py runserver 0.0.0.0:8000;
