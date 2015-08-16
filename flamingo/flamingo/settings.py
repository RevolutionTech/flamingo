"""
Django settings for flamingo project.
:Created: 15 August 2015
:Author: Lucas Connors

"""

import os

import flamingo.settings_secret as secret

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP_DIR = os.path.dirname(BASE_DIR)
SECRET_KEY = secret.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
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


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'flamingo',
        'USER': secret.DATABASE_USER,
        'PASSWORD': secret.DATABASE_PASSWORD,
        'HOST': secret.DATABASE_HOST,
        'PORT': secret.DATABASE_PORT,
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
MEDIA_ROOT = os.path.join(TOP_DIR, 'media')
MEDIA_URL = '/media/'
STATICFILES_DIRS = (
    os.path.join(TOP_DIR, 'static'),
)
STATIC_URL = '/static/'
