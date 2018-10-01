import os

from flamingo.settings.base import BaseSettings


class ProdSettings(BaseSettings):

    DEBUG = False
    ALLOWED_HOSTS = ['*',] # Heroku handles this under the hood

    # Static and media files
    DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
    STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
    AWS_S3_BUCKET_NAME = 'flamingo-photo'
    AWS_S3_BUCKET_NAME_STATIC = AWS_S3_BUCKET_NAME

    @property
    def AWS_ACCESS_KEY_ID(self):
        return os.environ['FLAMINGO_AWS_ACCESS_KEY_ID']

    @property
    def AWS_SECRET_ACCESS_KEY(self):
        return os.environ['FLAMINGO_AWS_SECRET_ACCESS_KEY']

    # Sentry
    @property
    def RAVEN_CONFIG(self):
        return {
            'dsn': 'https://{public_key}:{secret_key}@app.getsentry.com/{project_id}'.format(
                public_key='7404ed97fa2044418aa231daa72658fc',
                secret_key=os.environ['FLAMINGO_RAVEN_SECRET_KEY'],
                project_id='64150',
            ),
        }
