#!/usr/bin/env bash
set -e -o pipefail
# First build containers, compile messages, collect static files (copy them to static_root) and migrate database
docker-compose -f docker-compose.dev.yml -f docker-compose.prod.yml up -d --build
docker exec backend python3 manage.py migrate
docker exec --env PYTHONPATH="/match4healthcare-backend:$PYTHONPATH" backend django-admin makemessages --no-location
docker exec --env PYTHONPATH="/match4healthcare-backend:$PYTHONPATH" backend django-admin compilemessages
docker exec backend python3 manage.py collectstatic --no-input
docker exec backend python3 manage.py migrate
docker exec backend python3 manage.py check
# Restart container AFTER static files have been collected
docker-compose -f docker-compose.dev.yml -f docker-compose.prod.yml down
docker-compose -f docker-compose.dev.yml -f docker-compose.prod.yml up -d
