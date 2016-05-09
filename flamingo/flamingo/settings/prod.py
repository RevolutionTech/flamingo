import os

from flamingo.settings.base import BaseSettings


class ProdSettings(BaseSettings):

    DEBUG = False
    ALLOWED_HOSTS = ['*',] # Heroku handles this under the hood

    # Static and media files
    STATICFILES_STORAGE = 'flamingo.custom_storages.StaticStorage'
    DEFAULT_FILE_STORAGE = 'flamingo.custom_storages.MediaStorage'

    @property
    def AWS_ACCESS_KEY_ID(self):
        return os.environ['FLAMINGO_AWS_ACCESS_KEY_ID']

    @property
    def AWS_SECRET_ACCESS_KEY(self):
        return os.environ['FLAMINGO_AWS_SECRET_ACCESS_KEY']

    @property
    def STATIC_URL(self):
        return 'https://{aws_s3}/{static}/'.format(
            aws_s3=self.AWS_S3_CUSTOM_DOMAIN,
            static=self.STATICFILES_LOCATION
        )

    @property
    def MEDIA_URL(self):
        return 'https://{aws_s3}/{media}/'.format(
            aws_s3=self.AWS_S3_CUSTOM_DOMAIN,
            media=self.MEDIAFILES_LOCATION
        )

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
