"""
Django settings for FoodFlow project.
FoodFlow is an expiry-aware food donation platform connecting donors and recipients.
"""

import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Detect Vercel serverless environment
IS_VERCEL = 'VERCEL' in os.environ or os.environ.get('VERCEL_ENV') is not None

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if IS_VERCEL:
        raise ImproperlyConfigured("SECRET_KEY environment variable is required on Vercel.")
    SECRET_KEY = 'django-insecure-foodflow-university-cse-lab-secret-key-2026'

# SECURITY WARNING: don't run with debug turned on in production!
if IS_VERCEL:
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')
else:
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

# Allow Vercel, localhost, and custom domains
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS')
if allowed_hosts_env:
    ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_env.split(',') if h.strip()]
else:
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '.vercel.app',
        'food-flow-web.vercel.app',
    ]
    if DEBUG:
        ALLOWED_HOSTS.append('*')

# Security and CSRF settings for Vercel HTTPS reverse proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

csrf_origins_env = os.environ.get('CSRF_TRUSTED_ORIGINS')
if csrf_origins_env:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_origins_env.split(',') if o.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [
        'https://*.vercel.app',
        'https://food-flow-web.vercel.app',
        'http://127.0.0.1:8000',
        'http://localhost:8000',
    ]

# Session and CSRF cookie security in production
if not DEBUG and IS_VERCEL:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # FoodFlow Applications
    'accounts.apps.AccountsConfig',
    'locations.apps.LocationsConfig',
    'listings.apps.ListingsConfig',
    'claims.apps.ClaimsConfig',
    'notifications.apps.NotificationsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for serving static files on Vercel
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.views.unread_notification_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database configuration
# - Local development: SQLite
# - Production on Vercel: Persistent PostgreSQL via DATABASE_URL
database_url = os.environ.get('DATABASE_URL')

if database_url:
    DATABASES = {
        'default': dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
elif IS_VERCEL:
    raise ImproperlyConfigured(
        "DATABASE_URL environment variable is missing on Vercel. "
        "FoodFlow requires a persistent PostgreSQL database (e.g. Neon PostgreSQL) in production. "
        "Please configure DATABASE_URL in your Vercel Project Settings -> Environment Variables. "
        "Do not store production data in temporary /tmp SQLite storage."
    )
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization and Timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise storage configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Email backend for development (outputs to terminal console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@foodflow.local'

# FoodFlow specific business logic settings
FOODFLOW_SETTINGS = {
    'URGENCY_WARNING_HOURS': 6,
    'URGENCY_URGENT_HOURS': 2,
    'PICKUP_WINDOW_MINUTES': 90,
    'MIN_EXPIRY_MINUTES': 30,
    'MAX_EXPIRY_HOURS': 72,
}
