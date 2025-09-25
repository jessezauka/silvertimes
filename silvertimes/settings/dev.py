from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-janzqh1v-d6_kds%l9-fb!d2f3kh2*ezr+7qeh2^039ft4*fb9"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = 'noreply@silvertimes.art'
PASSWORD_RESET_TIMEOUT = 60 * 60 * 24  # 24 hours

# Security basics
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False # set True behind HTTPS
CSRF_COOKIE_SECURE = False # set True behind HTTPS

# Use in-memory cache in development to avoid needing the database_cache table.
# (Base settings configure a DatabaseCache named 'database_cache'.)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "dev-locmem-cache",
    }
}


try:
    from .local import *
except ImportError:
    pass
