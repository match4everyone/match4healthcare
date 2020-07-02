#!/usr/bin/env bash

echo -n "Waiting for backend to be running"
while [ -z "$(docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps --services --filter "status=running"|grep backend)" ]; do
    echo -n .
    sleep .2
done
echo " OK"

WAIT_FOR="\[INFO\] Listening at"
echo -n "Wait for '$WAIT_FOR' in backend log"
while [ -z "$(docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs backend|grep "${WAIT_FOR}")" ]; do
    echo -n .
    sleep 1
done
echo " Found"
