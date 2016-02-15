import os

import raven

from flamingo.settings.base import BaseSettings


class ProdSettings(BaseSettings):

    DEBUG = False
    ALLOWED_HOSTS = ['*',] # Heroku handles this under the hood

    # Sentry
    # @property
    # def RAVEN_CONFIG(self):
    #     return {
    #         'dsn': 'https://{public_key}:{secret_key}@app.getsentry.com/{project_id}'.format(
    #             public_key='7404ed97fa2044418aa231daa72658fc',
    #             secret_key=os.environ['FLAMINGO_RAVEN_SECRET_KEY'],
    #             project_id='64150',
    #         ),
    #         'release': raven.fetch_git_sha(self.TOP_DIR),
    #     }
