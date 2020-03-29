#!/usr/bin/env bash
docker exec backend sh -c 'python3 manage.py dumpdata > /match4healthcare-backend/backups/fixture-$(date +%F).json'
docker exec postgres sh -c 'pg_dumpall > /backup/pg_backup-$(date +%F).bak'