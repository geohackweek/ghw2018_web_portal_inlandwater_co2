#!/usr/bin/env bash
# wait-for-postgres.sh
# Adapted from https://docs.docker.com/compose/startup-order/

# Expects the necessary PG* variables.
set -e
cmd="$@"

until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c '\l'; do
  echo >&2 "$(date +%Y-%m-%dT%H-%M-%S) Postgres is unavailable - sleeping"
  sleep 1
done
echo >&2 "$(date +%Y-%m-%dT%H-%M-%S) Postgres is up - executing command"

exec $cmd