from .base import *
from .base import env

ADMINS = [
    ("Mike Bilenko", "mike@codnity.com")
]

CSRF_TRUSTED_ORIGINS = [
    "https://baclendfloristika.life",
    "https://www.baclendfloristika.life",
    "https://floristika.life",
    "http://localhost:3000",
    "http://192.168.0.204:3000"
]

CORS_ALLOWED_ORIGINS = [
    "http://baclendfloristika.life",
    "https://www.baclendfloristika.life",
    "https://baclendfloristika.life",
    "https://floristika.life",
    "http://localhost:3000",
    "http://192.168.0.204:3000"
]

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [
    "baclendfloristika.life",
    "www.baclendfloristika.life",
    "127.0.0.1",
    "localhost",
    "104.248.251.160",
]

DATABASES = {
    'default': env.db("DATABASE_URL")
}

ADMIN_URL = "supersecret/"

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO", "https"
)
# SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# 51840
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF",
    default=True
)



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'floristika.staf@gmail.com'
EMAIL_HOST_PASSWORD = 'olrj cysq djvf uxrq'
SITE_NAME = "Floristika"

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter":"verbose",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    },
}