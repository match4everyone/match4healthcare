#!/usr/bin/env bash
# First build
docker-compose -f docker-compose.dev.yml -f docker-compose.prod.yml up -d
docker exec --env PYTHONPATH="/match4healthcare-backend:$PYTHONPATH" backend django-admin makemessages
docker exec --env PYTHONPATH="/match4healthcare-backend:$PYTHONPATH" backend django-admin compilemessages
# Collect static BEFORE the container starts
docker exec backend python3 manage.py collectstatic --no-input
docker exec backend python3 manage.py migrate
# Start container AFTER static files have been collected
docker-compose -f docker-compose.dev.yml -f docker-compose.prod.yml restart



# docker-compose -f docker-compose.dev.yml -f docker-compose.prod.yml run