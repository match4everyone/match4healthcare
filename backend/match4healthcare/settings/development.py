import os
from os import path

from match4healthcare.constants.enum import Environment
from match4healthcare.settings.common import *  # noqa
from match4healthcare.settings.common import BASE_DIR, RUN_DIR

THIS_ENV = Environment.DEVELOPMENT

# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "(ki437obe@zig%4t)fiydfmok1*l6l=d5#uqyz^i-!y@j$n7ku"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": path.join(RUN_DIR, "db.sqlite3"),}
}

# =============== MAIL RELAY SERVER CONFIGURATION ===============
# Don't use our domain, prevent bad reputation
NOREPLY_MAIL = "match4healthcare-DEVELOPMENT<noreply@example.de>"

# Possible values are 'file', 'external', 'sendgrid'
# For storing mails local in files files, sending external (uberspace) or sending over sendgrid (production like)
MAIL_RELAY_OPTION = "file"

# +++ Store files locally
if MAIL_RELAY_OPTION == "file":
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(RUN_DIR, "sent_emails")

# +++ Use local debug server
elif MAIL_RELAY_OPTION == "external":
    EMAIL_HOST = "spahr.uberspace.de"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = "noreply@medisvs.spahr.uberspace.de"
    EMAIL_HOST_PASSWORD = "jonathan"
    EMAIL_USE_TLS = False

# +++ Use sendgrid
elif MAIL_RELAY_OPTION == "sendgrid":
    # Use API instead of SMTP server
    use_sendgrid_api = True

    # Retrieve sendgrid api key
    NOREPLY_MAIL = "match4healthcare<noreply@testing.match4healthcare.de>"
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

    if use_sendgrid_api:
        # Using the API
        EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
        # Disable sendbox mode to send actual emails
        SENDGRID_SANDBOX_MODE_IN_DEBUG = False

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
    # TODO: add logger message instead? # noqa: T003
    print("No email option selected")
    exit(1)


WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": False,
        "BUNDLE_DIR_NAME": "/",  # must end with slash
        "STATS_FILE": os.path.normpath(
            os.path.join(os.path.join(os.path.dirname(BASE_DIR), "frontend"), "webpack-stats.json")
        ),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        # 'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
        "LOADER_CLASS": "webpack_loader.loader.WebpackLoader",
    }
}
