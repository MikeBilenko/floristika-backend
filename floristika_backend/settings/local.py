from .base import *
from .base import env

# SECURITY WARNING: keep the secret key used in .production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY",default="nIju4v4-HD0Q7qYNT2NqoC1C_h3Q4ucUGFYZmoD0pKi11YuS8B0",)

# SECURITY WARNING: don't run with debug turned on in .production!
DEBUG = True

ALLOWED_HOSTS = [
    "24.144.76.8",
    "baclendfloristika.life",
    "127.0.0.1",
    "localhost",
    "159.65.206.54",
    "134.209.253.68"
]

# # Allow requests from specific origins
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

# # Trust CSRF cookies from these origins
CSRF_TRUSTED_ORIGINS = [
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

# CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'floristika.staf@gmail.com'
EMAIL_HOST_PASSWORD = 'olrj cysq djvf uxrq'
SITE_NAME = "Floristika"
