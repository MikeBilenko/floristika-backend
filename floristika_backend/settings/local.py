from .base import *
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY",default="nIju4v4-HD0Q7qYNT2NqoC1C_h3Q4ucUGFYZmoD0pKi11YuS8B0",)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080", "http://127.0.0.1:8080","http://localhost:5173","http://localhost:3000"]
# CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']


CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'floristika.staf@gmail.com'
EMAIL_HOST_PASSWORD = 'olrj cysq djvf uxrq'
SITE_NAME = "Floristika"
