#!/usr/bin/env bash
set -e -o pipefail
python3 manage.py migrate
python3 manage.py check

exec "$@"
