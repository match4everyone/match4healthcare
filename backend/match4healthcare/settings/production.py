import logging
import os

from django.utils.log import DEFAULT_LOGGING

from match4healthcare.settings.common import *  # noqa
from match4healthcare.settings.common import MIDDLEWARE, RUN_DIR

logger = logging.getLogger(__name__)

DEFAULT_LOGGING["handlers"]["console"]["filters"] = []

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = [
    "matchmedisvsvirus.dynalias.org",
    "helping-health.from-de.com",
    "match4healthcare.de",
    "match4healthcare.eu",
    "match4healthcare.org",
    "medis-vs-covid19.de",
    "localhost",
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_DB", ""),
        "USER": os.environ.get("POSTGRES_USER", ""),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": "database",
        "PORT": "5432",
    }
}

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# =============== MAIL RELAY SERVER CONFIGURATION ===============
# ToDo add environment variable based detection whether we are on prod or staging
NOREPLY_MAIL = "match4healthcare<noreply@match4healthcare.de>"
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# Use API instead of SMTP server
use_sendgrid_api = True

if (
    "TRAVIS" not in os.environ
    or ("TRAVIS" in os.environ and not bool(os.environ["TRAVIS"]))
    or (
        "TRAVIS" in os.environ
        and bool(os.environ["TRAVIS"])
        and os.environ["TRAVIS_PULL_REQUEST_SLUG"] is ["match4everyone/match4healthcare"]
    )
):
    NOT_FORK = True
else:
    NOT_FORK = False

if NOT_FORK:
    if use_sendgrid_api:
        # Using the API
        EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

        # Disable all tracking options
        SENDGRID_TRACK_EMAIL_OPENS = False
        SENDGRID_TRACK_CLICKS_HTML = False
        SENDGRID_TRACK_CLICKS_PLAIN = False

    else:
        # Normal SMTP
        EMAIL_HOST = "smtp.sendgrid.net"
        EMAIL_HOST_USER = "apikey"
        EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True
else:
    logger.warning(
        "Thanks for forking our repository. Pay attention that Travis CI doesn't test your code "
        "with sendgrid. If you want to use sendgrid for your tests, "
        "add your repository name to the list in the if statement for NOT_FORK"
    )
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(RUN_DIR, "sent_emails")
