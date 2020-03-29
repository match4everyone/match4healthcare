# Technische Dokumentation

## Docker
### First start
- Build images and run containers
`docker-compose -f docker-compose.dev.yml up --build`
- Start previously built containers in background
`docker-compose start`
- Apply migrations
`docker exec backend python3 manage.py migrate`
- Collect static files
`docker exec backend python3 manage.py collectstatic`
- Load test data:
`docker exec backend python3 manage.py loaddata fixture.json`

### Development
File changes in python files trigger an auto-reload of the server.
Migrations have to be executed with `docker exec backend python3 /matchedmedisvirus-backend/manage.py migrate`.

After changes to the Docker configuration, you have to restart and build the containers with `docker-compose -f docker-compose.dev.yml up --build`.

### Production

To run a container in production and in a new environment execute the `setup.sh` script which builds the containers, runs all configurations and then starts the web service.

If you want to deploy manually follow these steps closly:

1. Build the containers
2. Make messages
3. Compile messages
4. Collect static
5. Migrate
6. Restart containers (important, whitenoise does not reload static files after it has started)

## Local
- create migration after model change:
`python3 manage.py makemigrations`

- migrate to current version:
`python3 manage.py migrate`

- dump current database into fixture file (override fixture file):
`python3 manage.py dumpdata > fixture.json`

- load test data:
`python3 manage.py loaddata fixture.json`

- create superuser (to access staff page)
`python3 manage.py createsuperuser`

## Translation
- Add translatable strings in python with `_("Welcome to my site.")` and import `from django.utils.translation import gettext as _` ([Documentation](https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#internationalization-in-python-code))
- Add translatable strings in templates with `{% blocktrans %}This string will have {{ value }} inside.{% endblocktrans %}` or alternatively with the `trans` block and include `{% load i18n %}` at the top ([Documentation](https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#internationalization-in-template-code))
- Update the translation file
`django-admin makemessages -l en`
- Edit translations in `backend/locale/en/LC_MESSAGES/django.po`

## Production
Set `SECRET_KEY` in `backend.prod.env` for django and `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` for postgres on your host machine.
Start the system with `docker-compose -f docker-compose.dev.yml -f docker-compose.prod.yml up --build` and run `./deploy.sh`.
