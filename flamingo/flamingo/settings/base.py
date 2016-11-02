"""
:Created: 6 September 2015
:Author: Lucas Connors

"""

import os

from cbsettings import DjangoDefaults
import dj_database_url


class BaseSettings(DjangoDefaults):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    TOP_DIR = os.path.dirname(BASE_DIR)
    SECRET_KEY = os.environ['FLAMINGO_SECRET_KEY']

    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

    # Application definition
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'whitenoise.runserver_nostatic',
        'django.contrib.staticfiles',
        'raven.contrib.django.raven_compat',
        'sorl.thumbnail',
        'storages',
        'users.apps.UsersConfig',
        'photo.apps.PhotoConfig',
        'contest.apps.ContestConfig',
    )
    MIDDLEWARE = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
    )
    ROOT_URLCONF = 'flamingo.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [TOP_DIR + '/templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
    WSGI_APPLICATION = 'flamingo.wsgi.application'

    # Cache and Database
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
    DATABASES = {
        'default': dj_database_url.config(
            env='FLAMINGO_DATABASE_URL',
            default='postgres://postgres@localhost/flamingo',
            conn_max_age=500
        ),
    }

    # Internationalization
    TIME_ZONE = 'UTC'
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images) and Media
    MEDIA_ROOT = os.path.join(TOP_DIR, 'media')
    MEDIA_URL = '/media/'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATIC_ROOT = os.path.join(TOP_DIR, 'staticfiles')
    STATICFILES_DIRS = (
        os.path.join(TOP_DIR, 'static'),
    )
    STATIC_URL = '/static/'
    STATICFILES_LOCATION = 'static'
    MEDIAFILES_LOCATION = 'media'
    AWS_HEADERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }
    AWS_STORAGE_BUCKET_NAME = 'flamingo-photo'
    AWS_S3_CUSTOM_DOMAIN = '{bucket}.s3.amazonaws.com'.format(bucket=AWS_STORAGE_BUCKET_NAME)
    MAXIMUM_IMAGE_SIZE = 2 * 1024 * 1024 # 2MB

    # Authentication
    LOGIN_URL = '/login/'
