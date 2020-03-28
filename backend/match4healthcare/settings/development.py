from match4healthcare.settings.common import *
from os.path import abspath, basename, dirname, join, normpath


# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(ki437obe@zig%4t)fiydfmok1*l6l=d5#uqyz^i-!y@j$n7ku'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'run', 'db.sqlite3'),
    }
}

# =============== MAIL RELAY SERVER CONFIGURATION ===============
SENDGRID_SECRET_FILE = normpath(join(BASE_DIR, 'run', 'SENDGRID.key'))
#SENDGRID_API_KEY = open(SENDGRID_SECRET_FILE).read().strip()

# Normal SMTP
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Using the API
# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
