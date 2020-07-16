from .common import *  # noqa


SECRET_KEY = env("DJANGO_SECRET_KEY", "local")

TEST_RUNNER = "django.test.runner.DiscoverRunner"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_HOST_USER = "NONE"
ADMIN_EMAIL = "TESTING@NONE.NONE"
