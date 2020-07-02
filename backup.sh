#!/usr/bin/env bash
# This backup script will create a database dump from the postgres container
# the created backup will then be moved to the current directory
set -o errexit

echo "Creating PostgreSQL Dump"
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec database sh -c 'pg_dumpall -U $POSTGRES_USER> /backups/pg_backup-$(date +%F_%H%M%S).sql'
DB_CONTAINER="$(docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps -q database)"
docker run --rm --volumes-from $DB_CONTAINER -v $(pwd):/backup-bind-mount alpine sh -c "mv -v backups/* /backup-bind-mount/database/backups"


#Should we keep this? Have we ever verified this works?
#docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec backend  sh -c 'python3 manage.py dumpdata > /backend/backups/fixture-$(date +%F_%H%M%S).json'
