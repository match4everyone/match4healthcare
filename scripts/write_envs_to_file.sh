#!/bin/bash

echo "POSTGRES_DB=${POSTGRES_DB}" > database.prod.env
echo "POSTGRES_USER=${POSTGRES_USER}" >> database.prod.env
echo "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" >> database.prod.env

echo "SECRET_KEY=${SECRET_KEY}" > backend.prod.env
echo "SENDGRID_API_KEY=${SENDGRID_API_KEY}" >> backend.prod.env
echo "RABBITMQ_DEFAULT_USER=${RABBITMQ_DEFAULT_USER}" >> backend.prod.env
echo "RABBITMQ_DEFAULT_USER=${RABBITMQ_DEFAULT_USER}" >> backend.prod.env
