"""
Django settings for family_book project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

from dotenv import load_dotenv

import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')

CSRF_TRUSTED_ORIGINS = [
    'http://192.168.1.26'
]
# Application definition

INSTALLED_APPS = [
    "accounts",
    "core",
    "photos",
    "albums",
    "comments_likes",
    "sorl.thumbnail",
    "mathfilters",

    "django_browser_reload",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "storages",

    'django_cleanup.apps.CleanupConfig',
]

# Custom User model
AUTH_USER_MODEL = 'accounts.CustomUser'

DISPOSABLE_EMAIL_DOMAINS = "accounts/blacklist/disposable_email_domains.txt"

# Use the SMTP email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

# Set your Gmail credentials as environment variables
# EMAIL_HOST_USER = 'aeternam.service@gmail.com'
EMAIL_HOST_USER = os.getenv('AETERNAM_GMAIL_USER')
# EMAIL_HOST_PASSWORD = 'zolb dvdq yztt bwtx'
EMAIL_HOST_PASSWORD = os.getenv('AETERNAM_GMAIL_PASSWORD')

MIDDLEWARE = [
    "django_browser_reload.middleware.BrowserReloadMiddleware",

    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if not DEBUG:
    MIDDLEWARE.insert(2,"whitenoise.middleware.WhiteNoiseMiddleware")

ROOT_URLCONF = "aeternam.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.notifications",
            ],
        },
    },
]

WSGI_APPLICATION = "aeternam.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.postgresql_psycopg2",
    #         "NAME": "aeternam_dev_db",
    #         "USER": "hadi",
    #         "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    #         "HOST": "localhost",
    #         "PORT": "5432",
    #     }
    # }
else:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'), conn_max_age=600),
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

from django.utils.translation import gettext_lazy as _

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGE_CODE = 'en-us'

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('fr', _('French')),
    ('en', _('English'))
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
USE_S3 = os.getenv('USE_S3', '0').lower() in ['true', 't', '1']

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = None
    AWS_S3_REGION_NAME = 'eu-west-3'
    # AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_QUERYSTRING_EXPIRE = 600 #10mins
    AWS_S3_FILE_OVERWRITE = True
    AWS_LOCATION = 'media'
    DEFAULT_FILE_STORAGE =  'storages.backends.s3.S3Storage'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    THUMBNAIL_FORCE_OVERWRITE = True

    # STORAGES = {
    #     "default": {
    #         "BACKEND": "storages.backends.s3.S3Storage",
    #         "OPTIONS": {},
    #     },
    #     "staticfiles": {
    #         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    #     },
    # }

else:
    #     STORAGES = {
    #     "default": {
    #         "BACKEND":  "django.core.files.storage.FileSystemStorage",
    #         "OPTIONS": {},
    #     },
    #     "staticfiles": {
    #         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    #     },
    # }
    DEFAULT_FILE_STORAGE =  'django.core.files.storage.FileSystemStorage'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

if not DEBUG and not USE_S3:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    INSTALLED_APPS.append("whitenoise.runserver_nostatic")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
