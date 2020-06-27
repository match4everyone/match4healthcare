#!/usr/bin/env bash
source database.prod.env
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec backend  sh -c 'python3 manage.py dumpdata > /backend/backups/fixture-$(date +%F_%H%M%S).json'
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec database sh -c "pg_dumpall -U $POSTGRES_USER> /backups/pg_backup-$(date +%F_%H%M%S).sql"
