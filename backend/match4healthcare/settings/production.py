from match4healthcare.settings.common import *
from django.utils.log import DEFAULT_LOGGING

import logging

logger = logging.getLogger('django')

DEFAULT_LOGGING['handlers']['console']['filters'] = []

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['matchmedisvsvirus.dynalias.org', 'helping-health.from-de.com', 'match4healthcare.eu',
                 'medis-vs-covid19.de']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', ''),
        'USER': os.environ.get('POSTGRES_USER', ''),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': 'database',
        'PORT': '5432',
    }
}

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'applogfile': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'run', 'match4healthcare.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['applogfile'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
