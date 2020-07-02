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

# While collectstatic should rather run in the Dockerfile build
# it depends on the right DJANGO_SETTINGS_MODULE as it is subject to the
# STATICFILES_STORAGE setting. Whitenoise is only configured in production as of now
# so we would need to build the image in production mode, this would require setting a DJANGO_SECRET key
echo PYTHONPATH: $PYTHONPATH
django-admin collectstatic --no-input
django-admin migrate
django-admin check

exec "$@"
