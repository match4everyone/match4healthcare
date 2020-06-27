#!/usr/bin/env bash
set -e -o pipefail

if ! [[ -z "${PRODUCTION}" ]]; then
  echo Running in production mode, waiting for database to come up
  # Moved from docker-compose, as this is needed for migrate
  while ! (< /dev/tcp/database/5432) &> /dev/null; do
    echo "Waiting for database..."
    sleep 1
  done
fi

python3 manage.py migrate
python3 manage.py check

exec "$@"
