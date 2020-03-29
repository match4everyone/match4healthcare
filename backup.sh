#!/usr/bin/env bash
docker exec backend python3 manage.py dumpdata > /match4healthcare-backend/backups/fixture-$(date +%F).json
docker exec postgres pg_dumpall > /backup/pg_backup-$(date +%F).bak