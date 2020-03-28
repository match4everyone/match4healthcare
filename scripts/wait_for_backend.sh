#!/usr/bin/env bash
while ! $(docker ps | grep keyword | wc -l) -gt 0; do
    sleep 1
done