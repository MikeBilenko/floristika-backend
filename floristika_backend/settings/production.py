from .base import *
from .base import env

ADMINS = [
    ("Mike Bilenko", "mike@codnity.com")
]

CSRF_TRUSTED_ORIGINS = [
    "https://https://baclendfloristika.life",
    "https://floristika.life",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "http://baclendfloristika.life",
    "https://baclendfloristika.life:8080",
    "https://floristika.life",
    "https://plankton-app-znmwk.ondigitalocean.app",
    "http://159.65.206.54:8080",
    "http://24.144.76.8:8080",
    "http://134.209.253.68:8080",
]

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [
    "24.144.76.8",
    "baclendfloristika.life",
    "127.0.0.1",
    "localhost",
    "159.65.206.54",
    "134.209.253.68"
]

DATABASES = {
    'default': env.db("DATABASE_URL")
}

ADMIN_URL = "supersecret/"

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO", "https"
)
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# 51840
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF",
    default=True
)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


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