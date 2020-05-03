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

In order to run pre-commit checks every time, please run `pre-commit install` once in the repository. Pay attention when using `git commit -a`, because then the automatic code formatting will be added irreversably to your changes. The recommended workflow would be to use `git add` first, resulting in staged changes and unstaged codeformatting that you can double-check if you wish. You can of course always run `pre-commit run` to manually check all staged files before attempting a commit.

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
`django-admin makemessages -l en --no-location`
- Edit translations in `backend/locale/en/LC_MESSAGES/django.po`

## Production
Set `SECRET_KEY` and `SENDGRID_API_KEY` in `backend.prod.env` for Django
`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`  inside `database.prod.env` for postgres on your host machine.
Also add a `SLACK_LOG_WEBHOOK` to enable slack logging.

To run a container in production and in a new environment execute the `setup.sh` script which builds the containers, runs all configurations and starts the web service.

If you want to deploy manually follow these steps closly:

1. Build the containers
2. Make messages
3. Compile messages
4. Collect static
5. Migrate
6. Restart the backend container (important, whitenoise does not reload static files after it has started)

## Testing

For executing the tests use `python3 manage.py test`.

In case you add more required environment variables for productions, please check for their existance in `backend/apps/checks.py`.

## Logging

Logging should always use the following pattern if possible:

```
import logging
logger = logging.getLogger(__name__)
logger.info('message',extra={ 'request': request })
```

If the request is not logged as an extra parameter, the log entry will **NOT** be messaged to slack!

Adding the request as extra parameter will automatically extract logged on user information as well as POST variables and take care of removing sensitive information from
the logs, respecting the @method_decorator(sensitive_post_parameters()). For example in user sign in, this will prevent logging of passwords.

**Warning:** Special care must be taken to avoid errors from circular references. The extra parameters are written to the log file and serialized as JSON. Circular references will cause
logging failure. One example would be adding the student to the extra dict:

Student has an attribute for the user, user has an attribute for the student, ...

These circular references will prevent the log entry from being written.
Including request is always safe, because the logging formatter contains dedicated code for request logging.