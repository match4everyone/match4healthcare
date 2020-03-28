#!/usr/bin/env bash
while ! [ $(docker ps | grep backend | wc -l) -gt 0 ]; do
    sleep 1
done