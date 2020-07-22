import os

import dj_database_url

from .common import Common


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL', default='postgres://postgres:@postgres:5432/postgres'),
            conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600)),
        )
    }

    SECRET_KEY = os.getenv(
        "DJANGO_SECRET_KEY",
        default="SJJmKX0UvbrjgVkD4L36pqSO19iDFDYE6gqijZpMvAR5o9StDC4gLqJPYsM6bEE8",
    )

    INSTALLED_APPS = Common.INSTALLED_APPS
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "",
        }
    }

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
