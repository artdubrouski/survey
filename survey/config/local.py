from .common import Common


class Local(Common):
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
