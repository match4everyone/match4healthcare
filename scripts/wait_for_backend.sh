#!/usr/bin/env bash

while [ -z "$(docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps --services --filter "status=running"|grep backend)" ]; do
    sleep .2
done

echo -n "Waiting for backend"
while ! (< /dev/tcp/127.0.0.1/8000) &> /dev/null; do
  echo -n .
  sleep .2
done
echo " OK"
