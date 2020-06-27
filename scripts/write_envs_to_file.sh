#!/usr/bin/env bash

DATABASE_ENV_VARS="POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD"
BACKEND_ENV_VARS="SECRET_KEY SENDGRID_API_KEY SLACK_LOG_WEBHOOK LEAFLET_TILESERVER MAPBOX_TOKEN"

# Write env variables into env file
# This way you can set them in the travis configuration and they
# will be written into the appropriate env files by  this script

for ENVVAR in ${DATABASE_ENV_VARS}; do
    echo "${ENVVAR}=${!ENVVAR}" >> database.prod.env
done

for ENVVAR in ${BACKEND_ENV_VARS}; do
    echo "${ENVVAR}=${!ENVVAR}" >> backend.prod.env
done
