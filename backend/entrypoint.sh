#!/usr/bin/env bash
set -e -o pipefail

if ! [[ -z "${PRODUCTION}" ]]; then
  echo Running in production mode, waiting for database to come up
  # Moved from docker-compose, as this is needed for migrate
  echo -n "Waiting for database"
  while ! (< /dev/tcp/database/5432) &> /dev/null; do
    echo -n .
    sleep .2
  done
  echo " OK"
fi

echo PYTHONPATH: $PYTHONPATH
django-admin migrate
django-admin check

exec "$@"
