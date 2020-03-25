#!/bin/bash
docker exec --env PYTHONPATH="/matchmedisvsvirus-backend:$PYTHONPATH" backend django-admin makemessages
docker exec backend python3 manage.py migrate
docker exec backend python3 manage.py collectstatic --no-input
