"""
:Created: 6 September 2015
:Author: Lucas Connors

"""

import os

from cbsettings import DjangoDefaults
import raven


class BaseSettings(DjangoDefaults):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    TOP_DIR = os.path.dirname(BASE_DIR)

    DEBUG = True
    ALLOWED_HOSTS = []

    # Application definition
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'raven.contrib.django.raven_compat',
        'sorl.thumbnail',
        'users',
        'photo',
        'contest',
    )
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
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
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'flamingo',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    # Internationalization
    TIME_ZONE = 'UTC'
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images) and Media
    MEDIA_ROOT = os.path.join(TOP_DIR, 'media')
    MEDIA_URL = '/media/'
    STATICFILES_DIRS = (
        os.path.join(TOP_DIR, 'static'),
    )
    STATIC_URL = '/static/'
    MAXIMUM_IMAGE_SIZE = 2 * 1024 * 1024 # 2MB

    # Authentication
    LOGIN_URL = '/login/'

    # Sentry
    RAVEN_PUBLIC_KEY = '7404ed97fa2044418aa231daa72658fc'
    RAVEN_SECRET_KEY = 'FAKESECRET' # Overriden in prod.py
    RAVEN_PROJECT_ID = '64150'

    @property
    def RAVEN_CONFIG(self):
        return {
            'dsn': 'https://{public_key}:{secret_key}@app.getsentry.com/{project_id}'.format(
                public_key=self.RAVEN_PUBLIC_KEY,
                secret_key=self.RAVEN_SECRET_KEY,
                project_id=self.RAVEN_PROJECT_ID,
            ),
            'release': raven.fetch_git_sha(self.TOP_DIR),
        }
