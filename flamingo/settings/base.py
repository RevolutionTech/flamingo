"""
:Created: 6 September 2015
:Author: Lucas Connors

"""

import os

from cbsettings import DjangoDefaults
import dj_database_url


def aws_s3_bucket_url(settings_class, bucket_name_settings):
    bucket_name = getattr(settings_class, bucket_name_settings, "")
    if bucket_name:
        return f"https://{bucket_name}.s3.amazonaws.com"
    return ""


class BaseSettings(DjangoDefaults):

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    SECRET_KEY = os.environ["FLAMINGO_SECRET_KEY"]

    DEBUG = True
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

    # Application definition
    INSTALLED_APPS = (
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "whitenoise.runserver_nostatic",
        "django.contrib.staticfiles",
        "sorl.thumbnail",
        "django_s3_storage",
        "users.apps.UsersConfig",
        "photo.apps.PhotoConfig",
        "contest.apps.ContestConfig",
    )
    MIDDLEWARE = (
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
    )
    ROOT_URLCONF = "flamingo.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR + "/templates"],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        }
    ]
    WSGI_APPLICATION = "flamingo.wsgi.application"

    # Cache and Database
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "127.0.0.1:11211",
        }
    }
    DATABASES = {
        "default": dj_database_url.config(
            env="FLAMINGO_DATABASE_URL",
            default="postgres://postgres@localhost/flamingo",
            conn_max_age=500,
        )
    }

    # Internationalization
    TIME_ZONE = "UTC"
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images) and Media
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
    AWS_S3_KEY_PREFIX = "media"
    AWS_S3_KEY_PREFIX_STATIC = "static"
    AWS_S3_BUCKET_AUTH = False
    AWS_S3_MAX_AGE_SECONDS = 60 * 60 * 24 * 365  # 1 year
    MAXIMUM_IMAGE_SIZE = 2 * 1024 * 1024  # 2MB

    @property
    def MEDIA_URL(self):
        return "{aws_s3}/{media}/".format(
            aws_s3=aws_s3_bucket_url(self, "AWS_S3_BUCKET_NAME"),
            media=self.AWS_S3_KEY_PREFIX,
        )

    @property
    def STATIC_URL(self):
        return "{aws_s3}/{static}/".format(
            aws_s3=aws_s3_bucket_url(self, "AWS_S3_BUCKET_NAME_STATIC"),
            static=self.AWS_S3_KEY_PREFIX_STATIC,
        )

    # Authentication
    LOGIN_URL = "/login/"
