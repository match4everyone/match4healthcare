#!/usr/bin/env bash
while [ -z "$(docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps --services --filter "status=running"|grep backend)" ]; do
    sleep 1
done
